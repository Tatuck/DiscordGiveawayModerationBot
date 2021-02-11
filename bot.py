import discord
import asyncio
from discord.ext import commands
import json
from datetime import datetime, timedelta
import random
import re

client = commands.Bot(command_prefix="!")

jsonCredenciales = json.loads(open("botConfig.json","r",encoding="utf-8").read())
idBot = jsonCredenciales["idBot"]
token = jsonCredenciales["token"]
adminMute = jsonCredenciales["adminsMute"]
adminPro = jsonCredenciales["adminsPro"]
sorteadores = jsonCredenciales["sorteos"] #lol
rolConEnlaces = str(jsonCredenciales["rolConEnlaces"])
nombreRolSilenciado = jsonCredenciales["rolSilenciado"]

@client.event
async def on_ready():
    print("Estoy encendido!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="lo que quieras jeje"))

#MUTE
async def silenciarUsuario(user, razon=".", temp=2):
    await user.add_roles(discord.utils.get(user.guild.roles, name=nombreRolSilenciado)) #LE PONE EL ROL DE SILENCIADO
    #CREA UN EMBED (Mensaje bonito :D que se hace mediante la API)
    embedVar = discord.Embed(title=f"🔇ESTÁS SILENCIADO🔇", color=discord.Colour.red())
    embedVar.add_field(name=f"Razón: ", value=f"{razon}!", inline=True)
    embedVar.add_field(name=f"Duración silencio: ", value=f"{temp} minutos!", inline=True)
    embedVar.set_footer(text="No vuelvas a hacerlo o volverás a ser sancionado!")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    #ENVÍA EL EMBED A EL USUARIO POR UN MENSAJE PRIVADO
    await user.send(embed=embedVar)
    #ESPERA EL TIEMPO QUE SE HAYA CONFIGURADO PARA DESPUÉS ELIMINAR EL ROL SILENCIADO
    await asyncio.sleep(temp*60)
    await user.remove_roles(discord.utils.get(user.guild.roles, name=nombreRolSilenciado))

@client.command()
async def silenciar(ctx, user: discord.Member, razon="No especificada",temp="2"):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in adminMute)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    await ctx.send(f"{user.mention} **SILENCIADO** DURANTE **{temp}mins** RAZÓN: **{razon}**!")
    
    for x in user.roles:
        try:
            await user.remove_roles(x)
        except:
            pass
    await silenciarUsuario(user, razon=razon,temp=int(temp))

@client.command()
async def desilenciar(ctx, user: discord.Member):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in adminMute)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    await user.remove_roles(discord.utils.get(user.guild.roles, name=nombreRolSilenciado))

#https://stackoverflow.com/a/50790119/12994909
regexUrl="http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
cooldown = commands.CooldownMapping.from_cooldown(5, 10, commands.BucketType.member)
@client.event
async def on_message(msg):
    if msg.author.bot: #SI ES UN MENSAJE DE UN BOT NO HACE NADA
        return
    if msg.guild ==None:
        print(f"Mensaje: {msg.author}: {msg.content}")
        return
    if rolConEnlaces not in msg.author.roles:
        if len(re.findall(regexUrl,msg.content))>0:
            await msg.delete()
            await msg.channel.send(f"{msg.author.mention} No puedes publicar enlaces!!")
    if nombreRolSilenciado in str(msg.author.roles): #SI ESTÁ SILENCIADO ELIMINA EL MENSAJE
        await msg.delete()
        return
    retry_after = cooldown.update_rate_limit(msg)
    if retry_after: #SI HA MANDADO DEMASIADO MENSAJES ELIMINA 10 MENSAJES VERIFICANDO QUE SEAN DE ÉL Y LLAMA A SILENCIAR USUARIO
        def check(msgb):
            return msgb.author.id == msg.author.id
        await msg.channel.purge(limit=10, check=check, before=None)
        await silenciarUsuario(msg.author, razon="Mandar muchos mensajes")
        return
    await client.process_commands(msg) #SI NO PASA NADA DE LO ANTERIOR PROCESA EL COMANDO DEL MESNAJE(SI TIENE)

#KICK
@client.command()
async def kick(ctx, user: discord.Member,razon=""):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in adminPro)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    embedVar = discord.Embed(title=f"HAS SIDO KICKEADO de {ctx.guild.name}", color=discord.Colour.red())
    embedVar.add_field(name=f"Razón: ", value=f"{razon}!", inline=True)
    embedVar.set_footer(text="No vuelvas a hacerlo o volverás a ser sancionado!")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    await user.send(embed=embedVar)
    try:
        await ctx.send(f"{user.mention} Kickeado del servidor!")
        await user.kick(reason=razon)
    except Exception as e:
        print(e)
        pass

#BAN
@client.command()
async def ban(ctx, user: discord.Member,razon=""):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in adminPro)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    embedVar = discord.Embed(title=f"HAS SIDO BANEADO de {ctx.guild.name}", color=discord.Colour.red())
    embedVar.add_field(name=f"Razón: ", value=f"{razon}!", inline=True)
    embedVar.set_footer(text="...")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    await user.send(embed=embedVar)
    try:
        await ctx.send(f"{user.mention} Baneado del servidor!")
        await user.ban(reason=razon)
    except Exception as e:
        print(e)
        pass

@client.command()
async def unban(ctx, id):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in adminPro)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    try:
        user = await client.fetch_user(id)
    except:
        await ctx.send("Hubo un error: No se ha encontrado a ese ID")
        return
    try:
        await ctx.send(f"{user.mention} Desbaneado del servidor!")
        await ctx.guild.unban(user)
    except Exception as e:
        print(e)
        pass

#SORTEOS
pararSorteoLista = []
pararSorteoListaF= []
@client.command()
async def sorteoparar(ctx, id, forzar="No"):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in sorteadores)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    if forzar.lower() == "forzar":
        pararSorteoListaF.append(int(id))
    elif forzar.lower() == "no":
        pararSorteoLista.append(int(id))

sorteosLista= {}
@client.command()
async def sorteo(ctx, titulo, fecha):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in sorteadores)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    fechaDate = datetime.utcnow()+timedelta(minutes=int(fecha))
    fechaSecs = int(fecha)*60

    print(f"SORTEO en #{ctx.message.channel.name} título: {titulo} termina: {fecha}")
    print(fechaDate)
    embedVar = discord.Embed(title=f"🎉SORTEO **ACTIVO: {titulo}**", description="Reacciona con 🎉 para participar!", color=0x01f9b3, timestamp=(fechaDate))
    embedVar.add_field(name=f"⌚El sorteo termina en:",value=f"**{fecha}**!", inline=True)
    embedVar.add_field(name="**SORTEO GRACIAS A:**",value=f"{ctx.message.author.mention}",inline=True)
    embedVar.set_footer(text="Reacciona abajo para participar!")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    sorteoMsg = await ctx.message.channel.send(embed=embedVar)
    await sorteoMsg.add_reaction("🎉")

    tiempoRestante = fechaSecs
    
    while True:
        tiempo = ""   

        semanas, segundos = divmod(tiempoRestante, 604800)
        dias, segundos = divmod(segundos, 86400)
        horas, segundos = divmod(segundos, 3600)
        minutos, segundos = divmod(segundos, 60)
        
        #print(f"{dias} {horas} {minutos} {segundos}")

        comas =""
        if semanas > 0:
            tiempo = tiempo + f"{comas}**{semanas}** semana(s)"
            comas = ", "
        if dias > 0:
            tiempo = tiempo + f"{comas}**{dias}** día(s)"
            comas = ", "
        if horas > 0:
            tiempo = tiempo + f"{comas}**{horas}** hora(s)"
            comas = ", "
        if minutos > 0:
            tiempo = tiempo + f"{comas}**{minutos}** min(s)"
            comas = ", "
        if segundos > 0:
            tiempo = tiempo + f"{comas}**{segundos}** sec(s)"

        
        
        embedVar = discord.Embed(title=f"🎉SORTEO **ACTIVO: {titulo}**", description="Reacciona con 🎉 para participar!", color=0x01f9b3, timestamp=(fechaDate))
        embedVar.add_field(name=f"⌚El sorteo termina en:",value=f"{tiempo}!")
        embedVar.add_field(name="**SORTEO GRACIAS A:**",value=f"{ctx.message.author.mention}",inline=True)
        embedVar.set_footer(text="Reacciona abajo para participar!")
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
       
        global pararSorteoLista
        global pararSorteoListaF
        await sorteoMsg.edit(embed=embedVar)
        for x in range(30):
            if sorteoMsg.id in pararSorteoLista or sorteoMsg.id in pararSorteoListaF:
                print("PARAR")
                break
           
            await asyncio.sleep(1)

        if sorteoMsg.id in pararSorteoLista:
            print("PARAR SORTEO")
            break
        if sorteoMsg.id in pararSorteoListaF:
            print("PARAR SORTEO FORZOSAMENTE")
            embedVar = discord.Embed(title=f"❌SORTEO **FINALIZADO: {titulo}**", description=f"Este sorteo ya ha **terminado!**", color=discord.Color.red(), timestamp=(datetime.utcnow()))
            embedVar.add_field(name=f"❌ESTE SORTEO HA TERMINADO SIN GANADOR",value=f"SE HA TERMINADO FORZOSAMENTE")
            embedVar.add_field(name="**SORTEO GRACIAS A:**",value=f"{ctx.message.author.mention}",inline=True)
            embedVar.set_footer(text="SORTEO FINALIZADO TUS REACCIONES YA NO CONTARÁN")
            embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
            await sorteoMsg.edit(embed=embedVar)
            return
        tiempoRestante = tiempoRestante-30
        if tiempoRestante <= 0:
            print("FIN ESPERA")
            print(tiempoRestante)
            break

    msg = await sorteoMsg.channel.fetch_message(sorteoMsg.id)
    users = []
    for reaction in msg.reactions:
        async for user in reaction.users():
            users.append(user)
    #print(users)
    sorteosLista[sorteoMsg.id] = {}
    sorteosLista[sorteoMsg.id]["usuarios"] = {}
    for x in range(len(users)):
        sorteosLista[sorteoMsg.id]["usuarios"][x]=users[x].id
    sorteosLista[sorteoMsg.id]["datos"] = {}
    sorteosLista[sorteoMsg.id]["datos"]["nombre"]=titulo
    sorteosLista[sorteoMsg.id]["datos"]["channelid"]=sorteoMsg.channel.id
    #print(sorteosLista)
    sorteoTocado = 0
    while True:
        ganador = random.choice(users)
        if ganador.id == idBot:
            if sorteoTocado >=100:
                print("SOLO ME HA TOCADO A MÍ")
                break
            sorteoTocado = sorteoTocado+1
        else:
            break
    embedVar = discord.Embed(title=f"❌SORTEO **FINALIZADO: {titulo}**", description=f"Este sorteo ya ha **terminado!**", color=discord.Color.red(), timestamp=(datetime.utcnow()))
    embedVar.add_field(name=f"🎉GANADOR: ",value=f"{ganador.mention} FELICIDADES!")
    embedVar.add_field(name="**SORTEO GRACIAS A:**",value=f"{ctx.message.author.mention}",inline=True)
    embedVar.set_footer(text="❌SORTEO FINALIZADO TUS REACCIONES YA NO CONTARÁN")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    await sorteoMsg.edit(embed=embedVar)
    await sorteoMsg.channel.send(f"🎉GANADOR DEL **SORTEO ({titulo}) {ganador.mention} FELICIDADES!!**🎉")

    embedVar = discord.Embed(title=f"🎉HAS GANADO EL SORTEO: **{titulo}**🎉", description="**FELICIDADES!**", color=0x01f9b3, url=f"https://discordapp.com/channels/{ctx.message.guild.id}/{ctx.message.channel.id}/{ctx.message.id}")
    embedVar.set_author(name=f"SORTEO: {titulo}", url=f"https://discordapp.com/channels/{ctx.message.guild.id}/{ctx.message.channel.id}/{ctx.message.id}", icon_url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    embedVar.add_field(name=f"👇 👇 ",value=f"[DAME CLICK PARA IR A EL MENSAJE REACCIONADO!](https://discordapp.com/channels/{ctx.message.guild.id}/{ctx.message.channel.id}/{ctx.message.id})")
    embedVar.set_footer(text="Que lo disfrutes!")
    await ganador.send(embed=embedVar)

@client.command()
async def resorteo(ctx, idMsg):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in sorteadores)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    print(f"Reinicio sorteo en {ctx.channel.name} por {ctx.message.author} con ID {idMsg}")
    sorteoMensaje = await ctx.message.channel.fetch_message(int(idMsg))
    embedMensaje = sorteoMensaje.embeds
    users = []
    for reaction in sorteoMensaje.reactions:
        async for user in reaction.users():
            users.append(user)
    sorteoTocado = 0
    while True:
        ganador = random.choice(users)
        #print(ganador)
        if ganador.id == idBot:
            #print("ERA YO")
            if sorteoTocado >=100:
                print("SOLO ME HA TOCADO A MÍ")
                break
            sorteoTocado = sorteoTocado+1
        else:
            break
    print(f"Ganador sorteo reiniciado {ganador}")
    titulo = embedMensaje[0].title.split(": ")[1]
    embedVar = discord.Embed(title=f"🔁SORTEO **REINICIADO: {titulo}", description="Este sorteo ya ha **terminado!** de nuevo", color=discord.Color.red())
    embedVar.add_field(name=f"GANADOR: ",value=f"{ganador.mention} FELICIDADES!")
    embedVar.add_field(name="**SORTEO GRACIAS A:**",value=f"{ctx.message.author.mention}",inline=True)
    embedVar.set_footer(text="SORTEO FINALIZADO")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    await sorteoMensaje.edit(embed=embedVar)
    await sorteoMensaje.channel.send(f"🔁REINICIADO🔁 🎉GANADOR DEL **SORTEO ({titulo}) {ganador.mention} FELICIDADES!!**🎉")

@client.command()
async def resorteopar(ctx, idSor):
    roles = []
    for x in ctx.message.author.roles:
        roles.append(x.id)
    if any(item in roles for item in sorteadores)==False:
        await ctx.send("NO tienes permisos para usar este comando.")
        return
    
    idSort = int(idSor)
    sorteoTocado = 0
    #print(sorteosLista)
    titulo = sorteosLista[idSort]["datos"]["nombre"]
    channelid = sorteosLista[idSort]["datos"]["channelid"]
    canalSorteo = client.get_channel(channelid)
    sorteoMsg = await canalSorteo.fetch_message(idSort)
    while True:
        ganador = random.choice(sorteosLista[idSort]["usuarios"])
        #print(ganador)
        if ganador == idBot:
            #print("ERA YO")
            if sorteoTocado >=100:
                print("SOLO ME HA TOCADO A MÍ")
                break
            sorteoTocado = sorteoTocado+1
        else:
            break
    ganadorUser = client.get_user(ganador)
    #print(ganadorUser)
    
    embedVar = discord.Embed(title=f"🔁SORTEO **REINICIADO: {titulo}**", description="Este sorteo ya ha **terminado!** de nuevo", color=discord.Color.red())
    embedVar.add_field(name=f"GANADOR: ",value=f"{ganadorUser.mention} FELICIDADES!")
    embedVar.set_footer(text="SORTEO FINALIZADO")
    embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/idBot/b6560d97f36345f486cf34eb51c150d3.png?size=128")
    await sorteoMsg.edit(embed=embedVar)
    await sorteoMsg.channel.send(f"🔁REINICIADO🔁 🎉GANADOR DEL **SORTEO ({titulo}) {ganadorUser.mention} FELICIDADES!!**🎉")
    

client.run(token)
