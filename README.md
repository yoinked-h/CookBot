## CookBot | Prompt cookbook bot
A discord bot coded in pycord; the name is based on the [extension with similar name](https://github.com/dr413677671/PromptGallery-stable-diffusion-webui). 


### Setup
To setup the bot, clone the repo and modify the run.bat/run.sh file.

```bash
git clone https://github.com/yoinked-h/CookBot.git
cd CookBot
nano run.sh # modify the run.sh file
sh run.sh
```

### User Usage
#### /search <query\> (sendtochannel\):
Use it to seach the bot's storage.

`<query>` - the query you want to search.

`<sendtochannel>` - send the result to the channel. (optional: default: yes)


```bash
/search "Udongein"

/search "Reimu Hakurei" False
```
Returns an embed with the result, it has buttons for voting with a 👍 and a 👎. If a prompt has -10 score, it will be deleted.


#### /createcharacter <name\> <prompt\> <imageurl\>:
Use it to create a new character.

`<name>` - the name of the character.

`<prompt>` - the prompt used to generate the character.

`<imageurl>` - image url containing an image of the character.


```bash
/createcharacter "Udongein", "1girl, animal ears, ..." "https://i.imgur.com/..."

/createcharacter "Reimu Hakurei", "1girl, animal ears, ..." "https://cdn.discordapp.com/attachments/..."
```
