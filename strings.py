#             HERE ARE ALL EDITABLE FIELDS
# These IDs MUST be replaced according to the server IDs
id_guild = 846658239235096576  # The server's ID
id_role_king = 893640420695900230  # The King role ID
id_role_chal = 897153646968590398  # The Challenger role ID
id_role_adm = 861538231853121547  # The Admin role ID
id_channel_cotd = 861789796916789269  # The Card of the Day channel ID  -  902327229055385650, using test channel
id_channel_koth = 861789796916789269  # The King of the Hill channel ID  -  897162622540083210, but using test channel
id_channel_test = 861789796916789269  # Admin only channel for testing

# Bot options
prefix = 'w!'  # The prefix used for the bot commands
freq_cotd = 86400  # Card of the Day frequency, in seconds; 1d = 86400
freq_koth = 86400  # King of the Hill challenge time before expiration

# These are the text messages used by the bot
text_cotd = 'This is the card of the day:'  # The message that goes above the card
text_cotd_fail = 'Failed to fetch a card, just fyi: '  # The error message is displayed after the colon
text_king_nochal = 'You cannot win if there is no challenger.'  # Msg if king types victory without a challenger
text_king_nice_vic = 'Nice victory, champ, take this trophy: <:thumbsup:901618719426502687>'  # random w!v command
text_king_wins = 'is still the King! Win streak: '  # Sentence starts with mention to King and ends with the streak
text_king_new = 'is the new King of the Hill!'  # Sentence starts with mention to the new King
text_king_help = 'The current King is **{}** with **{}** victor'  # {}s are King role and win streak; victor + y/ies
text_king_away = ' lost their King role due to inactivity.'  # 24h without answering the challenge
text_king_remind = ", don't forget to accept or decline the challenge. Time remaining: "
text_adm_remind = ", don't forget to accept the challenge as soon as possible."
text_king_noaccept = "You need to accept the challenge first, "  # victory command before accepting; name, no mention
text_no_king = 'There is currently no King on the server. You may challenge the staff for the title.'  # No king on w!k
text_no_king_chal = 'No King right now. Challenging the staff for the title.'  # No king msg on challenge command
text_chal_self = 'Are you really trying to challenge yourself?'  # When the King sends challenge command
text_chal_twice = 'Chill bro, you already challenged His Highness.'  # When challenger sends challenge again
text_chal_sent = 'Your Highness, {}, you have been challenged by {}.'  # Challenge properly sent. Mentions king and chal
text_chal_wait = 'His Highness has already been challenged by'  # If challenge while challenge. Shows challenger
text_chal_accept = 'His Highness has accepted the challenge by'  # When King accepts the challenge. Shows challenger
text_chal_decline = 'The King has declined your challenge,'  # When King declines the challenge. Shows challenger
text_decline_twice = 'You may not decline another challenge, Your Highness.'  # When King tries to decline twice
text_give_up = 'gave up the King role.'  # Sentence preceded by the King who gave up the role
text_aint_no_king = "You ain't no King, buddy."  # When someone who's not a King try to give up the king role
text_support_welcome = '{}, the {} will soon come. Meanwhile, type in your concerns.'  # Msg sent when ticket is open
text_ticket_no_arg = "The ticket ID argument is missing. Type 'w!ct ####' to close ticket ####."  # Func *arg missing
text_ticket_none = 'There are no open tickets.'  # Call for w!ct with no open tickets
text_ticket_no_ID = 'Ticket ID not found.'  # The ID arg provided didn't match an existing ticket
text_ticket_no_perms = 'You do not have enough permissions to do this.'  # No permissions to use commands
