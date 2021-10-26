import os
import pandas as pd
import discord
from discord.ext import commands
from discord.ext import tasks
import requests
import json
import random
import strings as c


class CustomException(Exception):
    pass


class Filters:
    def __init__(self):
        self.vcount = 0
        self.challenge = False
        self.accept = False
        self.decline = False
        self.ready = False

    def victory_count(self, n):
        self.vcount += n

    def reset_count(self):
        self.vcount = 1

    def toggle_challenge(self):
        self.challenge = not self.challenge

    def toggle_accept(self):
        self.accept = not self.accept

    def toggle_decline(self):
        self.decline = not self.decline


class Tickets:
    def __init__(self):
        self.ticketnumb = 0
        self.opentickets = []
        self.ticketstr = None

    def create_ticket(self):
        self.ticketnumb += 1
        self.ticketstr = str("{:04d}".format(self.ticketnumb))
        self.opentickets.append(self.ticketstr)

    def get_ticketnumb(self):
        return self.ticketnumb

    def get_ticketstr(self):
        return self.ticketstr

    def get_opentickets(self):
        return self.opentickets

    def clear_ticket(self, ticket):
        self.opentickets.remove(str(ticket))


class Clock:
    tt = c.freq_koth

    def get_tt(self):
        return self.tt

    def get_half_tt(self):
        return round(int(self.tt / 2))

    def change_tt(self):
        self.tt = round(int(self.tt / 2))

    def reset_tt(self):
        self.tt = c.freq_koth


class Switches:
    def __init__(self):
        self.end = ''
        self.ct = 'x'

    def tt_switch(self):
        tt = cl.get_tt()
        if tt <= 60:
            self.ct = str(tt) + 's'
        elif 3600 > tt > 60:
            self.ct = str(round(int(tt / 60))) + 'm'
        elif tt >= 3600:
            self.ct = str(round(int(tt / 3600))) + 'h'
        else:
            print('erro no tt_switch')
        return self.ct

    def plural_switch(self, qtd):
        if qtd == 1:
            self.end = 'y'
        elif qtd > 1:
            self.end = 'ies'
        else:
            self.end = ''
            print('erro no arg da switch de plural: ' + str(qtd))
        return self.end


f = Filters()
t = Tickets()
cl = Clock()
s = Switches()
cards = pd.read_csv(os.path.abspath('cards.csv'), usecols=['scryfallId'])['scryfallId'].tolist()


class Wiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def roles(self):
        king = self.bot.get_guild(c.id_guild).get_role(c.id_role_king)
        chal = self.bot.get_guild(c.id_guild).get_role(c.id_role_chal)
        adm = self.bot.get_guild(c.id_guild).get_role(c.id_role_adm)
        return king, chal, adm

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(f'{self.bot.user} says: land, go!')
        await self.cotd.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    @tasks.loop(minutes=c.freq_cotd)
    async def cotd(self):
        while True:
            try:
                cardid = random.choice(cards)
                response = requests.get('https://api.scryfall.com/cards/' + str(cardid))
                link = json.loads(response.text)
                ban_tipos = ['Basic Land', 'Plane ']
                tipo = link['type_line']
                ban_cols = ['und', 'ugl', 'ust', 'unh']
                col = link['set']
                if any(ban_tipos) in tipo:
                    raise CustomException('Fetched Basic Land or Plane. Fetching another one...')
                if col in ban_cols:
                    raise CustomException('Fetched Un-series card. Fetching another one...')
                imagens = link['image_uris']
                grande = imagens['border_crop']
                channel = await self.bot.fetch_channel(c.id_channel_cotd)
                await channel.send(c.text_cotd)
                await channel.send(grande)
            except (KeyError, discord.DiscordServerError, CustomException) as e:
                print(c.text_cotd_fail + str(e.args[0]))
                continue
            break

    @tasks.loop(seconds=cl.get_half_tt())
    async def crono(self):
        king, chal, adm = self.roles()
        if f.challenge:
            if f.accept:
                self.crono.cancel()
                f.reset_count()
            elif king.members:
                rei = king.members[0]
                await self.bot.get_channel(c.id_channel_koth).send(f'{rei.mention}' +
                                                                   c.text_king_remind +
                                                                   s.tt_switch())
                cl.change_tt()
                self.crono.change_interval(seconds=cl.get_half_tt())
                if cl.get_tt() < 2:
                    desaf = chal.members[0]
                    await desaf.remove_roles(chal)
                    await rei.remove_roles(king)
                    await self.bot.get_channel(c.id_channel_koth).send(f'{rei.mention}' +
                                                                       c.text_king_away)
                    f.toggle_challenge()
                    f.reset_count()
                    self.crono.cancel()
            elif not king.members:
                await self.bot.get_channel(c.id_channel_koth).send(f'{adm.mention}' +
                                                                   c.text_adm_remind)
                self.crono.cancel()
        elif not f.challenge:
            self.crono.cancel()

    @commands.command(brief='Challenges the king',
                      name='challenge',
                      aliases=['c'])
    async def challenge(self, ctx):
        king, chal, adm = self.roles()
        if king in ctx.author.roles:
            await ctx.channel.send(c.text_chal_self)
        elif chal in ctx.author.roles:
            await ctx.channel.send(c.text_chal_twice)
        else:
            desaf = ctx.author
            if king.members:
                rei = king.members[0]
                if not f.challenge:
                    f.toggle_challenge()
                    await ctx.channel.send(c.text_chal_sent.format(rei.mention,
                                                                   desaf.mention))
                    await desaf.add_roles(chal)
                    await self.crono.start()
                if f.challenge:
                    current_chal = chal.members[0]
                    await ctx.channel.send(c.text_chal_wait +
                                           f' **{current_chal}**.')
            elif not king.members:
                await ctx.channel.send(c.text_no_king_chal)
                if not f.challenge:
                    f.toggle_challenge()
                    await ctx.channel.send(c.text_chal_sent.format(adm.mention,
                                                                   desaf.mention))
                    await desaf.add_roles(chal)
                    await self.crono.start()
                if f.challenge:
                    current_chal = chal.members[0]
                    await ctx.channel.send(c.text_chal_wait +
                                           f' **{current_chal}**.')

    @commands.command(brief='Registers a victory',
                      name='victory',
                      aliases=['v'])
    async def victory(self, ctx):
        king, chal, adm = self.roles()
        if king not in ctx.author.roles and chal not in ctx.author.roles and adm not in ctx.author.roles:
            self.victory.cancel()
        else:
            if king.members:
                old = king.members[0]
            else:
                old = adm.members[0]
            if not f.challenge:
                if ctx.author == old:
                    await ctx.channel.send(c.text_king_nochal)
            elif f.challenge:
                if not f.accept:
                    await ctx.channel.send(c.text_king_noaccept +
                                           f'**{old}**')
                if f.accept:
                    new = chal.members[0]
                    if ctx.author == old:
                        f.victory_count(1)
                        await ctx.channel.send(f'**{ctx.author}** ' +
                                               c.text_king_wins +
                                               str(f.vcount))
                        await new.remove_roles(chal)
                        f.toggle_challenge()
                        f.toggle_accept()
                    if ctx.author == new:
                        f.reset_count()
                        await old.remove_roles(king)
                        await new.remove_roles(chal)
                        await new.add_roles(king)
                        await ctx.channel.send(f'{ctx.author.mention} ' +
                                               c.text_king_new)
                        f.toggle_challenge()
                        f.toggle_accept()

    @commands.command(brief='Shows current king',
                      name='king',
                      aliases=['k'])
    async def king(self, ctx):
        king, chal, adm = self.roles()
        if king.members:
            rei = king.members[0]
            await ctx.channel.send(c.text_king_help.format(rei, f.vcount) +
                                   s.plural_switch(f.vcount) + '.')
        elif not king.members:
            await ctx.channel.send(c.text_no_king)

    @commands.command(brief='Accepts the challenge',
                      name='accept',
                      aliases=['a'])
    async def accept(self, ctx):
        king, chal, adm = self.roles()
        if f.challenge:
            desaf = chal.members[0]
            if king.members:
                if not f.accept:
                    if king in ctx.author.roles:
                        await ctx.channel.send(c.text_chal_accept +
                                               f' {desaf.mention}.')
                        f.toggle_accept()
            elif not king.members:
                if not f.accept:
                    if adm in ctx.author.roles:
                        await ctx.channel.send(c.text_chal_accept +
                                               f' {desaf.mention}.')
                        f.toggle_accept()

    @commands.command(brief='Declines the challenge',
                      name='decline',
                      aliases=['d'])
    async def decline(self, ctx):
        king, chal, adm = self.roles()
        if f.challenge:
            if king.members:
                if not f.decline:
                    if king in ctx.author.roles:
                        desaf = chal.members[0]
                        await ctx.channel.send(c.text_chal_decline +
                                               f' {desaf.mention}.')
                        f.toggle_decline()
                        await desaf.remove_roles(chal)
                        f.toggle_challenge()
                elif f.decline:
                    await ctx.channel.send(c.text_decline_twice)
            elif not king.members:
                if not f.decline:
                    if adm in ctx.author.roles:
                        desaf = chal.members[0]
                        await ctx.channel.send(c.text_chal_decline +
                                               f' {desaf.mention}.')
                        f.toggle_decline()
                        await desaf.remove_roles(chal)
                        f.toggle_challenge()
                elif f.decline:
                    await ctx.channel.send(c.text_decline_twice)

    @commands.command(brief='Gives up the king role',
                      name='give_up',
                      aliases=['g'])
    async def give_up(self, ctx):
        king, chal, adm = self.roles()
        if f.challenge:
            desaf = chal.members[0]
            if king.members:
                rei = king.members[0]
                if king in ctx.author.roles:
                    await ctx.channel.send(f'{rei.mention} ' +
                                           c.text_give_up)
                    await rei.remove_roles(king)
                    if desaf:
                        await desaf.remove_roles(chal)
                else:
                    await ctx.channel.send(c.text_aint_no_king)
            elif not king.members:
                await ctx.channel.send(c.text_aint_no_king)

    @commands.command(brief='Shows this message',
                      name='help',
                      aliases=['h'])
    async def help(self, ctx):
        with open('wiz_help.png', 'rb') as arquivo:
            await ctx.channel.send(file=discord.File(arquivo, 'wiz_help.png'))
            arquivo.close()

    @commands.command(brief='Opens a ticket',
                      name='ticket',
                      aliases=['t'])
    async def ticket(self, ctx):
        king, chal, adm = self.roles()
        t.create_ticket()
        canal = await ctx.guild.create_text_channel('ticket-' +
                                                    str(t.get_ticketstr()))
        temprole = await ctx.guild.create_role(name='ticket-' +
                                                    str(t.get_ticketstr()))
        await canal.set_permissions(temprole,
                                    view_channel=True,
                                    send_messages=True,
                                    read_messages=True,
                                    read_message_history=True)
        await canal.set_permissions(ctx.guild.default_role,
                                    view_channel=False)
        user = ctx.author
        await user.add_roles(temprole)
        await canal.send(c.text_support_welcome.format(ctx.author.mention, adm.mention))

    @commands.command(brief='Closes a ticket',
                      name='close_ticket',
                      aliases=['ct'])
    async def close_ticket(self, ctx, ticket_id=None):
        king, chal, adm = self.roles()
        if adm in ctx.author.roles:
            if ticket_id is None:
                await ctx.channel.send(c.text_ticket_no_arg)
            else:
                if len(t.get_opentickets()) < 1:
                    await ctx.channel.send(c.text_ticket_none)
                elif str(ticket_id) not in t.get_opentickets():
                    await ctx.channel.send(c.text_ticket_no_ID)
                elif str(ticket_id) in t.get_opentickets():
                    canal = discord.utils.get(ctx.guild.channels,
                                              name=f'ticket-{ticket_id}')
                    cargo = discord.utils.get(ctx.guild.roles,
                                              name=f'ticket-{ticket_id}')
                    user = cargo.members[0]
                    await user.remove_roles(cargo)
                    t.clear_ticket(str(ticket_id))
                    await canal.delete()
                    await cargo.delete()
        else:
            await ctx.channel.send(c.text_ticket_no_perms)


def setup(bot):
    bot.add_cog(Wiz(bot))
