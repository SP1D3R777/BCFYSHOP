#BOT DISCORD CREE PAR SP1D3R
import discord
from discord.ext import commands, tasks 
import requests
import random
from inspect import CO_NESTED
from typing import Literal
from discord.ext import commands
import discord
import asyncio
import string 
import re 
import os
import time
import subprocess
intents = discord.Intents.all()
intents.presences = True  # Activer les intents de présence
intents.typing = False  # Vous pouvez activer les autres intents si nécessaire


bot = commands.Bot(command_prefix='!', intents=intents)

#VERIF

# ID du rôle de citoyen
citizen_role_id = 1158811953117020162  # Remplacez par l'ID du rôle citoyen

# ID du canal de vérification
verification_channel_id = 1158811955851698188  # Remplacez par l'ID du canal de vérification

@bot.command(name='verification')
async def send_verification_embed(ctx):
    # Vérifie si l'auteur de la commande est déjà citoyen
    if discord.utils.get(ctx.author.roles, id=citizen_role_id):
        await ctx.send("Vous êtes déjà un citoyen.")
        return

    # Crée un embed de vérification avec une image
    embed = discord.Embed(
        title="Bienvenue sur JokerRP",
        description="Pour devenir citoyen, cliquez sur la réaction ci-dessous.",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1158811953679048713/1159072569455018014/joker-mascot-logo-design-vector-with-modern-illustration-concept-style-for-badge-emblem-and-tshirt-printing-angry-joker-illustration-with-guns-in-hand-400-177811201.jpg?ex=651e8df3&is=651d3c73&hm=fbb029fbb77e47ef24748655964ba7a9fda9bcb5eaf553d514795bd76e8b3880&")  # Remplacez par l'URL de votre image

    # Envoie l'embed dans le canal de vérification
    verification_channel = bot.get_channel(verification_channel_id)
    message = await verification_channel.send(embed=embed)

    # Ajoute la réaction à l'embed
    await message.add_reaction('✅')

@bot.event
async def on_raw_reaction_add(payload):
    # Vérifie si la réaction a été ajoutée dans le canal de vérification et par un utilisateur
    if payload.channel_id == verification_channel_id and payload.user_id != bot.user.id:
        # Récupère le membre qui a ajouté la réaction
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Vérifie si la réaction est ✅
        if str(payload.emoji) == '✅':
            # Récupère le rôle citoyen
            citizen_role = guild.get_role(citizen_role_id)

            # Ajoute le rôle au membre
            await member.add_roles(citizen_role)

            # Envoyer un message de confirmation
            confirmation_embed = discord.Embed(
                title="Vérification Réussie",
                description=f"{member.mention} est maintenant un citoyen.",
                color=discord.Color.green()
            )
            await member.send(embed=confirmation_embed)

@bot.command(name='tickets')
async def open_ticket(ctx):
    # Logique pour ouvrir un ticket
    await ctx.send("Pour ouvrir un ticket, veuillez contacter le support dans le salon approprié.")

@bot.command(name='sugges')
async def make_suggestion(ctx):
    # Logique pour envoyer une suggestion
    await ctx.send("Pour soumettre une suggestion, veuillez utiliser le salon de suggestions.")

@bot.event
async def on_message(message):
    if "bon jeu" in message.content.lower() and "jokerrp" in message.content.lower():
        await message.channel.send("Bon jeu à vous sur JokerRP!")

    await bot.process_commands(message)


# ID du salon où vous souhaitez envoyer les logs
log_channel_id = 1158811953679048707

@bot.event
async def on_message_delete(message):
    # Vérifiez que le message supprimé n'est pas un message du bot
    if message.author != bot.user:
        channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(
            title="Message Supprimé",
            description=f"Message supprimé dans {message.channel.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Auteur", value=message.author.mention, inline=False)
        embed.add_field(name="Contenu", value=message.content, inline=False)
        await channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Membre Rejoint",
        description=f"{member.mention} a rejoint le serveur.",
        color=discord.Color.green()
    )
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Membre Parti",
        description=f"{member.mention} a quitté le serveur.",
        color=discord.Color.orange()
    )
    await channel.send(embed=embed)

#BL
bot_owner_id = 1138368915475550218
# Une liste pour stocker les membres blacklistés
blacklisted_members = []

@bot.command()
async def bl(ctx, member: discord.Member):
    # Vérifiez si l'auteur de la commande est le propriétaire du bot ou un administrateur du serveur
    if ctx.author.id == bot_owner_id or ctx.author.guild_permissions.administrator:
        # Blacklistez le membre en l'empêchant de rejoindre le serveur
        await member.ban()

        # Envoyez un message privé au membre blacklisté
        try:
            await member.send("Vous avez été blacklisté sur ce serveur.")
        except discord.HTTPException:
            pass  # En cas d'erreur lors de l'envoi du message privé

        # Ajoutez le membre à la liste des blacklistés
        blacklisted_members.append(member.id)

        await ctx.send(f"{member.mention} a été blacklisté.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

@bot.command()
async def unbl(ctx, member: discord.Member):
    # Vérifiez si l'auteur de la commande est le propriétaire du bot ou un administrateur du serveur
    if ctx.author.id == bot_owner_id or ctx.author.guild_permissions.administrator:
        # Déblacklistez le membre en le retirant de la liste des blacklistés
        if member.id in blacklisted_members:
            blacklisted_members.remove(member.id)
        
        # Révoquez la blacklist du membre
        await member.unban()

        await ctx.send(f"{member.mention} a été déblacklisté.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

@bot.command()
async def bl_list(ctx):
    # Vérifiez si l'auteur de la commande est le propriétaire du bot ou un administrateur du serveur
    if ctx.author.id == bot_owner_id or ctx.author.guild_permissions.administrator:
        # Récupérez la liste des noms des membres blacklistés
        blacklist_names = []
        for member_id in blacklisted_members:
            member = await bot.fetch_user(member_id)
            if member:
                blacklist_names.append(member.name)

        if blacklist_names:
            blacklist_text = "\n".join(blacklist_names)
            await ctx.send(f"Membres blacklistés :\n{blacklist_text}")
        else:
            await ctx.send("Aucun membre n'est blacklisté.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
#RC

@bot.command()
async def rc(ctx):
    # Vérifie si la commande est !rc on
    if ctx.message.content == '!rc on':
        embed = discord.Embed(
            title="Les Recrutements sont Ouverts",
            description="Merci de déposer votre candidature dans un !ticket",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    # Vérifie si la commande est !rc off
    elif ctx.message.content == '!rc off':
        embed = discord.Embed(
            title="Les Recrutements sont désormais Fermés",
            description="Merci d'attendre la prochaine session !",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    # Si la commande est simplement !rc
    else:
        embed = discord.Embed(
            title=f"Bonjour / Bonsoir à Tous Cher {ctx.author.display_name} !",
            description="J'ai l’honneur de vous annoncer que nous sommes actuellement à la recherche de staff...",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Voici nos critères pour rejoindre notre équipe staff :",
            value="Être actif\nAvoir un minimum de connaissances dans le domaine\nÊtre Mature\nAvoir un Bon français que ce soit oral / Écrit\nÊtre responsable de ces actes\nAvoir un minimum de professionnalisme"
        )
        embed.add_field(
            name="Si vous répondez à tous ces critères d’éligibilité et que vous êtes prêt à nous rejoindre,",
            value="Merci de faire un ticket et ensuite nous vous prendrons en charge 😉 !"
        )
        embed.set_footer(text=f"Cordialement : L'équipe JokerRP")
        await ctx.send(embed=embed)


#SUGGESTION
@bot.command()
async def suggestion(ctx, *, message):
    # Trouver le salon pour les suggestions par son ID
    suggestion_channel = ctx.guild.get_channel(1158811956120125505)
    
    if suggestion_channel is not None:
        # Créer un embed pour la suggestion
        embed = discord.Embed(
            title="Nouvelle Suggestion",
            description=message,
            color=discord.Color.blue()
        )
        embed.add_field(name="Proposé par", value=ctx.author.mention, inline=False)
        
        # Envoyer l'embed dans le salon de suggestions
        suggestion_message = await suggestion_channel.send(embed=embed)
        
        # Ajouter les réactions "oui" et "non" automatiquement
        await suggestion_message.add_reaction("✅")  # Emoji pour "oui"
        await suggestion_message.add_reaction("❌")  # Emoji pour "non"
        

#SPAM

spam_threshold = 5  # Nombre maximal de messages autorisés en un court laps de temps
spam_cooldown = 30  # Durée en secondes du laps de temps pour le spam

spam_count = {}

@bot.event
async def on_message(message):
    # Ignorer les messages de bots
    if message.author.bot:
        return

    author_id = message.author.id

    # Vérifier si l'auteur du message est déjà dans le dictionnaire spam_count
    if author_id in spam_count:
        spam_count[author_id] += 1
    else:
        spam_count[author_id] = 1

    # Vérifier si l'utilisateur a atteint le seuil de spam
    if spam_count[author_id] >= spam_threshold:
        await message.delete()  # Supprimer le message de spam
        await message.channel.send(embed=discord.Embed(description=f"{message.author.mention}, arrêtez de spammer !"))  # Avertissement sous forme d'embed

        # Optionnel : Expulser l'utilisateur après plusieurs avertissements
        if spam_count[author_id] >= spam_threshold * 2:
            await message.author.kick(reason="Spam")

        # Optionnel : Bannir l'utilisateur après plusieurs expulsions
        if spam_count[author_id] >= spam_threshold * 3:
            await message.author.ban(reason="Spam répété")

        # Réinitialiser le compteur de spam pour cet utilisateur après le spam_cooldown
        await asyncio.sleep(spam_cooldown)
        spam_count[author_id] = 0

    await bot.process_commands(message)

#DISCORD

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    channel_id = 123  # ID du salon où vous souhaitez envoyer le message

    # Vérifier si le bot est en ligne ou hors ligne
    if bot.is_ready():
        status_embed = discord.Embed(
            title="JokerRP - Opérationnel",
            color=discord.Color.blue()
        )
    else:
        status_embed = discord.Embed(
            title="JokerRP Hors ligne",
            description=f"Code d'erreur : {bot.ws.close_code}",
            color=discord.Color.red()
        )

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(embed=status_embed)

 #INFO


@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    await update_rpc_status.start()

@tasks.loop(seconds=60)
async def update_rpc_status():
    activity = discord.Activity(
        type=discord.ActivityType.playing, 
        name="JokerRP"
    )

    await bot.change_presence(activity=activity)

#@bot.command(name="ano")
async def ano(ctx, *, text):
    await ctx.message.delete()
    embed = discord.Embed(description=text, color=0x000000)
    embed.set_author(name="🕵️ Message DarkChat")
    embed.set_footer(text="JokerRP @2023")
    await ctx.send(embed=embed)
    if len(ctx.message.attachments) == 0:
        return
    image_url = ctx.message.attachments[0].url
    embed = discord.Embed()
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

    




    # Commande d'aide
@bot.command(name='aide')  # Utilisez 'name' pour définir le nom de la commande
async def aide(ctx):
    embed = discord.Embed(title="💬 JokerRP - Aide", description="Voici la liste des commandes disponibles :")

    # Ajoutez des champs pour chaque commande
    embed.add_field(name="!say ", value="Permet d'envoyer un message avec le bot.", inline=False)
    embed.add_field(name="!mod ", value="Permet de voir toutes les commandes de modération.", inline=False)
    embed.add_field(name="!clear ", value="Permet d'effacer le nom de message inscrit", inline=False)
    embed.add_field(name="!renew ", value="Permet de nettoyer le salon souhaité", inline=False)
    await ctx.message.delete()
    
    #SPAM
    
  
    # Vous pouvez ajouter autant de champs que nécessaire

    await ctx.send(embed=embed)


@bot.command()
async def renew(ctx):
    # Vérifier si l'utilisateur a les autorisations nécessaires
    if ctx.author.guild_permissions.administrator:
        channel = ctx.channel

        # Effacer le chat
        await channel.purge()

        # Réinitialiser le salon en supprimant tous les messages épinglés
        pinned_messages = await channel.pins()
        for message in pinned_messages:
            await message.unpin()

        # Envoyer un message pour indiquer que le salon a été réinitialisé
        await channel.send("💬 JokerRP à reinisialisé le salon !")

    else:
        await ctx.send("Désolé, vous n'avez pas les autorisations nécessaires pour utiliser cette commande.")
#DEMASK :


@bot.command()
async def supp(ctx, message_id):
    # Vérifiez si l'auteur de la commande est un administrateur du serveur
    if ctx.author.guild_permissions.administrator:
        try:
            message = await ctx.channel.fetch_message(int(message_id))
            await message.delete()
            await ctx.send(f"Message {message_id} supprimé avec succès.")
        except discord.NotFound:
            await ctx.send("Message introuvable.")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {str(e)}")

# Événement qui se déclenche lorsque quelqu'un quitte le serveur
@bot.event
async def on_member_remove(member):
    # Récupérez le salon avec l'ID 1147505839851192351
    channel = member.guild.get_channel(1158811955851698187)

    if channel:
        # Créez un embed de départ animé avec la photo de profil
        message = f'Au revoir, {member.mention} a quitté le serveur JokerRP.'
        embed = create_blue_embed(member, message)
        await channel.send(embed=embed)

        #BIENVENUE :
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@bot.command()
async def gen(ctx, arg):
    # Vérifier si l'auteur de la commande est un utilisateur valide
    if ctx.message.author:
        # Créer un salon privé avec l'auteur de la commande
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.message.author: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(f'rockstar-{ctx.message.author}', overwrites=overwrites)

        # Envoyer le message et mentionner le propriétaire du message
        embed = discord.Embed(title="JokerRP - Voici votre compte rockstar (mail:password), merci de le récupéré rapidement, le salon ce supprime automatiquement dans 30 secondes.")
        await channel.send(f"{ctx.message.author.mention}", embed=embed)
        

        # Supprimer le salon après 10 secondes
        await asyncio.sleep(30)
        await channel.delete()

        # Fonction pour créer un embed bleu animé avec la photo de profil
def create_blue_embed(member, message):
    embed = discord.Embed(description=message, color=0x3498db)  # Couleur bleue
    embed.set_author(name=member.display_name)  # Photo de profil
    return embed

# Événement qui se déclenche lorsque quelqu'un rejoint le serveur
@bot.event
async def on_member_join(member):
    # Récupérez le salon avec l'ID 1147505839851192351
    channel = member.guild.get_channel(1158811955851698187)

    if channel:
        # Créez un embed de bienvenue animé avec la photo de profil
        message = f'Hey, bienvenue sur le serveur JokerRP, {member.mention}!'
        embed = create_blue_embed(member, message)
        await channel.send(embed=embed)

    username = member.name
    user_id = member.id
    created_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
    server_count = len(bot.guilds)
    
    salon_id = 1159083497873481728
    
    salon = bot.get_channel(salon_id)
    
    if salon is not None:
        embed = discord.Embed(title="JokerRP - LOGS", color=discord.Color.blue())
        embed.add_field(name="Utilisateur", value=username, inline=False)
        embed.add_field(name="ID du compte", value=user_id, inline=False)
        embed.add_field(name="Compte créé le", value=created_at, inline=False)
        embed.add_field(name="Membre de serveurs", value=server_count, inline=False)
        await salon.send(embed=embed)
    else:
        print(f'Le salon avec l\'ID {salon_id} est introuvable.')

        # Envoyez l'embed dans le salon
        await channel.send(embed=embed)

#RPC
    # Définir les messages à afficher dans la RPC
    rpc_messages = [
        "🃏・JokerRP - 2023",
        "👨‍🔬・Serveur RP",
        "🎫・!ticket",
    ]

#DEBAN

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command(name='deban')
async def deban(ctx):
    # Vérifier si la commande est utilisée dans le bon serveur
    if ctx.guild.id != 1159092503807533107:
        return

    # Créer un ticket dans la catégorie spécifiée
    category_id = 1159092503807533107
    category = discord.utils.get(ctx.guild.categories, id=category_id)
    ticket_channel = await category.create_text_channel(f'ticket-{ctx.author.name}', reason='Création d\'un ticket de déban')

    # Créer un embed avec les conditions pour être déban
    embed = discord.Embed(title='Demande de déban', color=0x00ff00)
    embed.add_field(name='Conditions pour être déban', value='1. Inclure une description détaillée de la situation\n2. Joindre des preuves et des captures d\'écran\n3. Indiquer la raison du bannissement')
    embed.set_footer(text='JokerRP Staff')

    # Envoyer l'embed dans le canal de ticket
    await ticket_channel.send(embed=embed)

    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    # Envoyez l'embed dans le ticket et pingez l'auteur
    ticket_message = await ticket_channel.send(content=ctx.author.mention, embed=embed)

    # Ajouter les permissions pour les membres du staff
    staff_role_ids = [1158811953188315279]  # Remplacez ceci par les rôles ID du personnel
    staff_roles = [discord.utils.get(ctx.guild.roles, id=role_id) for role_id in staff_role_ids]
    
    for role in staff_roles:
        await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)

    await ctx.send(f'Ticket de déban créé dans {ticket_channel.mention}')
# Salon de journal pour les tickets fermés
ticket_closed_logs_channel_id = 1158811953679048707
#TICKET 

@bot.command()
async def ticket(ctx):
    staff_role = ctx.guild.get_role(1153573100974252093)
    welcome_message = (
        "__Bienvenue dans le support de **JokerRP** !\n\n__"
        "Un membre de notre **équipe** sera avec vous sous peu pour vous aider avec vos questions et préoccupations. "
        "Utilisez la commande `!close` pour fermer le ticket.\n\n"
        "Nous avons de nombreux **comptes** de tout type, merci de spécifier ce dont vous avez besoin.\n\n"
        "Nhésitez pas à mettre un **avis** au **__STAFF__** qui vous à aider en faisant la **commande** `!avis` (nombre d'étoile de 1 à 5) suivis de votre texte\n\n"
        "__Merci et à bientôt__ !"
    )

    embed = discord.Embed(title="Nouveau Ticket - JokerRP", color=0x0000FF)
    embed.description = welcome_message
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1158811953679048713/1159072569455018014/joker-mascot-logo-design-vector-with-modern-illustration-concept-style-for-badge-emblem-and-tshirt-printing-angry-joker-illustration-with-guns-in-hand-400-177811201.jpg?ex=651e8df3&is=651d3c73&hm=fbb029fbb77e47ef24748655964ba7a9fda9bcb5eaf553d514795bd76e8b3880&")



    # Créez le ticket dans la catégorie spécifiée
    category = ctx.guild.get_channel(1159079696206671952)  # Catégorie spécifiée
    if not category:
        await ctx.send("La catégorie spécifiée n'a pas été trouvée.")
        return

    ticket_channel = await category.create_text_channel(f'ticket-{ctx.author.name}')
    
    # Réglez les autorisations pour le personnel
    await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    # Envoyez l'embed dans le ticket et pingez l'auteur
    ticket_message = await ticket_channel.send(content=ctx.author.mention, embed=embed)

    await ctx.send("Ticket ouvert avec succès!")
ticket_categories = 1159079696206671952

@bot.command()
async def close(ctx):
    if ctx.channel.name.startswith('ticket-'):
        # Récupérez le salon de journal des tickets fermés
        ticket_closed_logs_channel = ctx.guild.get_channel(ticket_closed_logs_channel_id)
        
        # Collectez les informations du ticket pour les journaux
        ticket_owner = ctx.channel.name.replace('ticket-', '')
        closer = ctx.author.name
        ticket_messages = []
        async for message in ctx.channel.history(limit=None):
            ticket_messages.append(f"{message.author.name}: {message.content}")
        
        # Créez un journal détaillé
        detailed_log = (
            f"**Ticket fermé par :** {closer}\n"
            f"**Ticket ouvert par :** {ticket_owner}\n"
            f"**Messages du ticket :**\n" + '\n'.join(ticket_messages)
        )
        
        # Envoyez le journal dans le salon de journal des tickets fermés
        await ticket_closed_logs_channel.send(f"Ticket fermé :\n{detailed_log}")
        
        # Supprimez le salon du ticket
        await ctx.channel.delete()
        await ctx.send("Ticket fermé avec succès!")
        return

    # Créez un message avec l'avis et l'auteur
    avis_embed = discord.Embed(title="Avis du Staff", description=avis_text, color=0x0000FF)
    avis_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1147571551550570628/1153628723287957514/logo.png")
    avis_embed.set_footer(text=f"Avis donné par {ctx.author.name}")
@bot.command()
async def avis(ctx, stars: int, *, avis_text):
    # Récupérez le salon avis-staff
    avis_channel = ctx.guild.get_channel(1158811955851698194)
    if not avis_channel:
        await ctx.send("Le salon avis-staff n'a pas été trouvé.")
        return

    # Créez un message avec l'avis et l'auteur
    avis_embed = discord.Embed(title="Avis du Staff", description=avis_text, color=0x0000FF)
    avis_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1158811953679048713/1159072569455018014/joker-mascot-logo-design-vector-with-modern-illustration-concept-style-for-badge-emblem-and-tshirt-printing-angry-joker-illustration-with-guns-in-hand-400-177811201.jpg?ex=651e8df3&is=651d3c73&hm=fbb029fbb77e47ef24748655964ba7a9fda9bcb5eaf553d514795bd76e8b3880&")
    avis_embed.set_footer(text=f"Avis donné par {ctx.author.name}")

    # Convertissez le nombre d'étoiles en emojis
    star_emoji = "⭐" * stars
    avis_embed.add_field(name="Note", value=star_emoji, inline=False)

    # Envoyez l'avis dans le salon avis-staff
    await avis_channel.send(embed=avis_embed)
    await ctx.send("Avis envoyé avec succès!")
        #------------------------------------

@tasks.loop(seconds=5)  # Mettez à jour la RPC toutes les 5 secondes
async def update_rpc(rpc_messages):
    if not hasattr(update_rpc, "counter"):
        update_rpc.counter = 0  # Initialiser le compteur

    message = rpc_messages[update_rpc.counter]
    update_rpc.counter = (update_rpc.counter + 1) % len(rpc_messages)

    activity = discord.Activity(
        name=message,
        type=discord.ActivityType.watching
    )

    await bot.change_presence(activity=activity)

# Démarrer la boucle de mise à jour de la RPC
@bot.event
async def on_connect():
    await asyncio.sleep(1)  # Attendre un court instant pour que l'event loop soit prêt

    # Définir les messages à afficher dans la RPC
    rpc_messages = [
        "🃏・JokerRP - 2023",
        "👨‍🔬・Serveur RP",
        "🎫・!ticket",
    ]
    
    update_rpc.start(rpc_messages)

    #MODERATION : 

@bot.command()
async def mod(ctx):
    await ctx.message.delete()
    mod_embed = discord.Embed(title='Commandes de Modération',
                              description='Liste des commandes de modération disponibles :',
                              color=discord.Color.blue())
    

    mod_embed.add_field(name='!kick [utilisateur]', value='Expulse un utilisateur du serveur.')
    mod_embed.add_field(name='!ban [utilisateur]', value='Bannit un utilisateur du serveur.')
    mod_embed.add_field(name='!mute [utilisateur]', value='Rend un utilisateur muet dans le salon actuel.')
    mod_embed.add_field(name='!unmute [utilisateur]', value='Définit la parole libre pour un utilisateur muet.')
    mod_embed.add_field(name='!clear [nombre]', value='Supprime un certain nombre de messages dans le salon.')
    mod_embed.add_field(name='!role on ou !role off', value='Pour activer ou désactiver lautorôle quand un membre rejoins le serveur')
    mod_embed.add_field(name='!say', value='Pour envoyer un message avec le bot JokerRP')
    
    await ctx.send(embed=mod_embed)
    
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} a été expulsé du serveur.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} a été banni du serveur.')

@bot.command()
async def mute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muted_role, send_messages=False)
        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} a été rendu muet dans le salon actuel.')
    else:
        await ctx.send("Vous n'avez pas les autorisations nécessaires pour exécuter cette commande.")

@bot.command()
async def clear(ctx, amount: int):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)  # +1 to account for the command message
        await ctx.send(f'{amount} messages ont été supprimés dans ce salon.', delete_after=1)
    else:
        await ctx.send("Vous n'avez pas les autorisations nécessaires pour exécuter cette commande.")

#DISCORD SUPP :
                
    
                # Supprimez le message du bot dans le salon où il a été envoy

@bot.command()
async def upload(ctx):
    # Vérifie que la commande a un fichier joint (image ou vidéo)
    if len(ctx.message.attachments) == 0:
        await ctx.send("Veuillez joindre une vidéo ou une image avec votre message.")
        return

    # Récupère le premier fichier joint
    attachment = ctx.message.attachments[0]

    # Vérifie que le fichier est une image ou une vidéo
    if not attachment.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov')):
        await ctx.send("Le fichier joint doit être une image (jpg, jpeg, png, gif) ou une vidéo (mp4, mov).")
        return

    # Envoie le fichier joint avec le message du bot
    await ctx.send(f"Message de {ctx.author.display_name} :")
    await ctx.send(file=await attachment.to_file())

#AUTOROLE : 

# ID du rôle à attribuer
role_id = 1158811953117020162
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@bot.command()
async def role(ctx, action):
    # Vérifiez si l'utilisateur a les autorisations nécessaires pour effectuer cette action
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("Vous n'avez pas la permission de gérer les rôles.")
        return
    
    # Obtenez le rôle en fonction de l'ID
    role = ctx.guild.get_role(role_id)

    if action == 'on':
        # Attribuez le rôle à l'utilisateur
        await ctx.author.add_roles(role)
        await ctx.send(f"Vous avez maintenant le rôle {role.name}.")
    elif action == 'off':
        # Retirez le rôle de l'utilisateur
        await ctx.author.remove_roles(role)
        await ctx.send(f"Vous n'avez plus le rôle {role.name}.")
    else:
        await ctx.send("Utilisation incorrecte de la commande !role. Utilisez !role on ou !role off.")

# ID du rôle à attribuer
role_id = 1158811953117020162

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

#@bot.event
##async def on_member_join(member):
    # Obtenez le serveur (guild) du membre
    #guild = member.guild

    # Obtenez le rôle en fonction de l'ID
    #role = discord.utils.get(guild.roles, id=role_id)

    #if role is not None:
        # Attribuez le rôle au membre
        #await member.add_roles(role)
        #print(f"Le rôle {role.name} a été attribué à {member.display_name}.")


 #CRYPTIA




#PING 


@bot.event
async def on_message(message):
    # Vérifiez si le message contient une mention du bot
    if bot.user.mentioned_in(message):
        embed = discord.Embed(
            title="Hey, je suis là, ne t'inquiète pas !",
            description="Utilise la commande !aide pour plus d'informations.",
            color=discord.Color.green()
        )
        embed.set_footer(text="www.JokerRP.fr")

        # Répondez avec l'embed
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


#VERIF 

@bot.command()
async def say(ctx, *, text):
    # Vérifie si l'utilisateur a la permission de gérer les messages
    if ctx.author.guild_permissions.manage_messages:
        # Crée un embed bleu
        embed = discord.Embed(
            title="JokerRP - Annonce",
            description=text,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
    else:
        # Si l'utilisateur n'a pas la permission de gérer les messages, envoie simplement le texte
        await ctx.send(text)

# Définir une variable pour suivre si la vérification est activée ou désactivée

@bot.command()
async def verif_off(ctx):
    global verification_active

    
    
    # Vérifier si la vérification est déjà désactivée
    if not verification_active:
        await ctx.send("La vérification est déjà désactivée.")
    else:
        await ctx.send("Vérification désactivée.")
        verification_active = False

def generate_captcha_embed():
    # Génération d'un captcha (exemple simple ici)
    captcha_characters = string.ascii_uppercase + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    captcha_text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=6))
    
    embed = discord.Embed(title="Captcha", description="Résolvez le captcha suivant pour vous vérifier.")
    embed.add_field(name="Captcha Text", value=captcha_text, inline=False)
    
    return embed

@bot.event
async def on_message(message):
    global verification_active
    
    if message.author == bot.user:
        return
    
    if verification_active and message.content.upper() == 'CAPTCHA':
        await message.author.send("Félicitations ! Vous avez résolu le captcha.")
        await message.author.add_roles(message.guild.get_role(1148713739118452839))  # Remplacez ROLE_ID_HERE par l'ID du rôle de vérification
        verification_active = False

    await bot.process_commands(message)



intents = discord.Intents.default()
intents.typing = False
intents.presences = False


role_non_verifie_id = 1148715455633178704  # Remplacez par l'ID du rôle "Non vérifié"
role_verifie_id = 1148713739118452839  # Remplacez par l'ID du rôle "Vérifié"

# Définir une variable pour suivre si la vérification est activée ou désactivée
verification_active = False

#LOGS
# ID du canal de logs
log_channel_id = 1159083497873481728

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_member_ban(guild, user):
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Membre Banni",
        description=f"{user.mention} a été banni du serveur.",
        color=discord.Color.red()
    )
    await log_channel.send(embed=embed)

@bot.event
async def on_member_kick(guild, user):
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Membre Expulsé",
        description=f"{user.mention} a été expulsé du serveur.",
        color=discord.Color.orange()
    )
    await log_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Membre Parti",
        description=f"{member.mention} a quitté le serveur.",
        color=discord.Color.dark_grey()
    )
    await log_channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Message Supprimé",
        description=f"Message supprimé par {message.author.mention} dans #{message.channel}",
        color=discord.Color.red()
    )
    await log_channel.send(embed=embed)

@bot.event
async def on_raw_message_delete(payload):
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Message Supprimé",
        description=f"Message supprimé par {payload.cached_message.author.mention} dans #{payload.cached_message.channel}",
        color=discord.Color.red()
    )
    await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        log_channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(
            title="Message Édité",
            description=f"Message édité par {before.author.mention} dans #{before.channel}\nAvant: {before.content}\nAprès: {after.content}",
            color=discord.Color.gold()
        )
        await log_channel.send(embed=embed)

@bot.event
async def on_raw_message_edit(payload):
    log_channel = bot.get_channel(log_channel_id)
    embed = discord.Embed(
        title="Message Édité",
        description=f"Message édité par {payload.cached_message.author.mention} dans #{payload.cached_message.channel}\nAvant: {payload.cached_message.content}\nAprès: {payload.data['content']}",
        color=discord.Color.gold()
    )
    await log_channel.send(embed=embed)

@bot.event
async def on_message(message):
    if "ping" in message.content.lower():
        log_channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(
            title="Ping Détecté",
            description=f'Ping détecté de la part de {message.author.mention} dans #{message.channel}',
            color=discord.Color.blue()
        )
        await log_channel.send(embed=embed)

    if "@everyone" in message.content or "@here" in message.content:
        log_channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(
            title="Mention Everyone/Here Détectée",
            description=f'Mention everyone/here détectée et supprimée dans #{message.channel} par {message.author.mention}',
            color=discord.Color.orange()
        )
        await log_channel.send(embed=embed)

    if message.mention_everyone or message.mention_here:
        log_channel = bot.get_channel(log_channel_id)
        embed = discord.Embed(
            title="Mention Everyone/Here Détectée",
            description=f'Mention everyone/here détectée de la part de {message.author.mention} dans #{message.channel}',
            color=discord.Color.orange()
        )
        await log_channel.send(embed=embed)


#LOGS TICKET

# ID du salon où vous souhaitez enregistrer les messages et afficher les logs.
target_channel_id = 1152261472102129724

# Une liste pour stocker les messages en attente d'être enregistrés
log_messages = []
@bot.event
async def on_message(message):
    # Vérifiez si le message commence par "!close"
    if message.content.startswith('!close'):
        # Récupérez les messages enregistrés dans la liste log_messages
        logs = '\n'.join(log_messages)
        
        # Créez un embed pour afficher les logs
        embed = discord.Embed(title='Logs du ticket', description=logs, color=discord.Color.blue())
        
        # Récupérez le salon cible
        target_channel = bot.get_channel(target_channel_id)
        
        # Envoyez l'embed dans le salon cible
        await target_channel.send(embed=embed)
        
        # Effacez les messages enregistrés
        log_messages.clear()

    else:
        # Ajoutez le contenu du message à la liste log_messages
        log_messages.append(f"{message.author.name}: {message.content}")

    # Continuez le traitement des messages normalement
    await bot.process_commands(message)


#!DARKCHAT 

@bot.event
async def on_message(message):
    # Vérifie si le message est dans le salon spécifié et n'est pas envoyé par le bot lui-même
    if message.channel.id == 1146740591846248549 and message.author != bot.user:
        # Crée un embed pour le message anonyme
        embed = discord.Embed(description=message.content)
        embed.set_author(name="🕵️ Message DarkChat")
        embed.set_footer(text="JokerRP @2023")
        
        # Envoie l'embed dans le salon
        await message.channel.send(embed=embed)
        # Supprime le message original de l'utilisateur pour plus d'anonymat
        await message.delete()

    await bot.process_commands(message)

#EMBED
# Dictionnaire de correspondance entre les noms de couleurs et les couleurs Discord
COULEURS = {
    'bleu': discord.Color.blue(),
    'jaune': discord.Color.gold(),
    'vert': discord.Color.green(),
    'noir': discord.Color.dark_grey(),
    'orange': discord.Color.orange()
}

# Crée la commande !embed
@bot.command()
async def embed(ctx, channel: discord.TextChannel = None):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send("Veuillez entrer le titre de l'embed:")
    title_message = await bot.wait_for('message', check=check)

    await ctx.send("Veuillez entrer la description de l'embed:")
    description_message = await bot.wait_for('message', check=check)

    await ctx.send("Veuillez entrer la couleur de l'embed (bleu, jaune, vert, noir, orange) :")
    couleur_message = await bot.wait_for('message', check=check)
    couleur_nom = couleur_message.content.lower()
    
    couleur = COULEURS.get(couleur_nom)

    if couleur is None:
        await ctx.send("Couleur non valide. Utilisez l'une des couleurs suivantes : bleu, jaune, vert, noir, orange.")
        return

    await ctx.send("Voulez-vous ajouter une image à l'embed ? Répondez avec 'oui' ou 'non'.")
    image_choice_message = await bot.wait_for('message', check=check)

    image_url = None
    if image_choice_message.content.lower() == 'oui':
        await ctx.send("Veuillez entrer l'URL de l'image:")
        image_message = await bot.wait_for('message', check=check)
        image_url = image_message.content

# Demande à l'utilisateur de spécifier le salon où envoyer l'embed
    await ctx.send("Mentionnez le salon où vous souhaitez envoyer l'embed :")

    try:
        channel_message = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé. Commande annulée.")
        return

    # Récupère le salon mentionné dans le message
    channel_mention = channel_message.content
    channel = discord.utils.get(ctx.guild.channels, mention=channel_mention)

    # Vérifie si le salon existe et est un salon de texte
    if channel and isinstance(channel, discord.TextChannel):
        # Crée un embed
        embed = discord.Embed(description=text, color=discord.Color.blue())



    # Crée l'embed avec les informations fournies
    embed = discord.Embed(title=title_message.content, description=description_message.content, color=couleur)

    if image_url:
        embed.set_image(url=image_url)

    # Envoie l'embed dans le canal
    await ctx.send(embed=embed)
    await channel.send(embed=embed)


##TWT :

# Remplacez 'YOUR_TOKEN' par le token de votre bot Discord
bot.run('MTE1OTA3MjgzMDUzMzY3MzA2MQ.GjHjwS.TV7B1q-NuME3fjJ5qFplYaCpVd9hdbfJiC-3-I')
#bot.run('MTE1MjU2NDY1OTQwMDk5ODkzMg.GtPOAn.LFqJ_JMHgQ6LF2LMf3JQN2VbJ8Yi8bDLTV0P-k')
#NODE 

#GEN


        #say
#INFO 
