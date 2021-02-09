# DiscordGiveawayModerationBot
A Discord bot which can make Giveaways, Ban, Unban, Kick, Mute, Unmute, Antispam and Delete messages with links. 
Un bot de Discord que puede crear Sorteos, Banear, Desbanear, Kickear, Mutear, Desmutear, Antispam y Eliminar mensajes con links.

## How can I use it? / ¿Cómo puedo usarlo?
### Python 3
- **EN:** Install packages.
- **ES:** Instala los paquetes.
`pip install -r requirements.txt` or `pip3 install -r requirements.txt`

- **EN:** Configure the file botConfig.json.
- **ES:** Configura el archivo botConfig.json.

#### Example/Ejemplo:
```
{
    "idBot":12345678910, <-THE BOT ID / EL ID DEL BOT
    "token":"<token>", <-THE BOT TOKEN / EL TOKEN DEL BOT
    "adminsMute":[12345678910,12345678910], <-ID OF THE ROLES (ONLY MUTE) / ID DE LOS ROLES (SOLO MUTEAR)
    "adminsPro":[12345678910,12345678910], <- ID OF THE ROLES (KICK/BAN) / ID DE LOS ROLES (KICK/BAN)
    "sorteos":[12345678910,12345678910], <- ID OF THE ROLES (GIVEAWAYS) / ID DE LOS ROLES (SORTEOS)
    "rolConEnlaces":12345678910, <- ID OF THE ROLE WHICH CAN POST LINKS / ID DEL ROL QUE PUEDE PUBLICAR LINKS
    "rolSilenciado":"🔇SILENCIADO" <- NAME OF YOUR MUTED ROLE / NOMBRE DEL ROL PARA MUTEAR
}
```

*Si tiene algún error, házmelo saber!*
