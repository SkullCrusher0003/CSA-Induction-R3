import discord
from aiohttp import web
import socketio
import asyncio
from routines import r1, r2

bot = discord.Bot()
sio = socketio.AsyncServer(async_mode = 'aiohttp')
app = web.Application()
sio.attach(app)

userData = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

# Registration Command
@bot.slash_command(name="register", description="Register your machine on the server")
async def register(ctx: discord.ApplicationContext, token: str):
    userData[ctx.author.id] = token
    await ctx.respond(content = f"<:Y4D_Verified:874316924006330368> Your Device has been successfully registered with token ID `{token}`.", delete_after = 5, ephemeral = True)

    
# Run Command
routine_dict= {
    'Routine 1': r1,
    'Routine 2': r2
}

class RoutineModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label = "Website URL"))
        self.add_item(discord.ui.InputText(label = "Seconds to Wait"))
        self.add_item(discord.ui.InputText(label = "Shell Command"))

    async def callback(self, interaction):
        r1[0][1] = self.children[0].value
        r1[1][1] = int(self.children[1].value)
        r1[2][1] = self.children[2].value
        await sio.emit('test event', r1, room=userData[interaction.user.id])
        disabled_embed = routine_run_embed()
        disabled_embed.colour = discord.Colour.green()
        await interaction.response.edit_message(embed = disabled_embed, view = RoutineDisabledView(), delete_after = 15)
        
class RoutineDisabledView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Routine is being executed.",
        min_values = 1,
        max_values = 1,
        disabled = True,
        options = [
            discord.SelectOption(
                label = "Routine 1",
                description = "Select to run the Sample Routine"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        pass

    
class RoutineView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Select the Routine you wish to run.",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label = "Routine 1",
                description = "Select to run the Sample Routine",
                emoji = "<:Y4D_One:886272148782596147>"
            ),
            discord.SelectOption(
                label = "Routine 2",
                description = "Select to run the Programming Workspace Routine",
                emoji = "<:Y4D_Two:886272149055225887>"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        selected_routine = routine_dict[f'{select.values[0]}']
        if selected_routine != r1:
            await sio.emit('test event', selected_routine, room=userData[interaction.user.id])
            self.disable_all_items()
            disabled_embed = routine_run_embed()
            disabled_embed.colour = discord.Colour.green()
            await interaction.response.edit_message(embed = disabled_embed, view = RoutineDisabledView(), delete_after = 10)
        else: 
            await interaction.response.send_modal(RoutineModal(title = "Required Inputs"))

def routine_view_embed():
    embed = discord.Embed(title = "Routines", description = "All available routines are shown below", colour = discord.Colour.blurple())
    embed.set_footer(text = "Use `/routines run` to start any routine.")
    embed.add_field(
        name = "<:Y4D_One:886272148782596147> Routine 1",
        value = "This Routine is a Sample \n**1.** Open a Website (argument: `URL`) \n**2.** Wait for a Few Seconds (argument: `Seconds`) \n**3.** Run a Shell Command (argument: `Command`)",
        inline = False
    )
    embed.add_field(
        name = "<:Y4D_Two:886272149055225887> Routine 2",
        value = "This Routine sets up your Programming Workspace. \n**1.** Open [StackOverflow](https://www.stackoverflow.com/) \n**2.** Wait for 3 Seconds \n**3.** Open `sample.py` in a Code Editor \n**4.** Wait for 3 Seconds \n**5.** Open [GitHub](https://www.github.com)",
        inline = False
    )
    return embed

def routine_run_embed():
    embed = discord.Embed(title = "Which Routine Do You Wish To Run?", description = "All available routines are shown below", colour = discord.Colour.blurple())
    embed.set_footer(text = "It may take upto 3 seconds for the routine to begin.")
    embed.add_field(
        name = "<:Y4D_One:886272148782596147> Routine 1 (Sample)",
        value = "\n**1.** Open a Website (takes argument: URL) \n**2.** Wait for a Few Seconds (takes argument: Seconds) \n**3.** Run a Shell Command (takes argument: Command)",
        inline = False
    )
    embed.add_field(
        name = "<:Y4D_Two:886272149055225887> Routine 2 (Programming Workspace)",
        value = "\n**1.** Open [StackOverflow](https://www.stackoverflow.com/) \n**2.** Wait for 3 Seconds \n**3.** Open `sample.py` in a Code Editor \n**4.** Wait for 3 Seconds \n**5.** Open [GitHub](https://www.github.com)",
        inline = False
    )
    return embed

routine_group = bot.create_group("routines", "Run Routines")

@routine_group.command()
async def view(ctx):
    await ctx.respond(embed = routine_view_embed())
@routine_group.command()
async def run(ctx):
    await ctx.respond(embed = routine_run_embed(), view = RoutineView(), ephemeral = True)

async def startup(request):
    return web.Response(text="Hello there!")

@sio.event
async def regr(sid, data):
    roomID = data['roomID']
    await sio.enter_room(sid, roomID)
    print(f"I entered room, {roomID}")

async def start_server(app):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host = '<your host address here>', port = 9350)
    await site.start()
    print("Server is now online!")

async def main(app):
    server_task = asyncio.create_task(start_server(app))
    bot_task = asyncio.create_task(bot.start("<your bot token here>"))
    await asyncio.gather(server_task, bot_task)

app.add_routes([web.get('/', startup)])

if __name__ == '__main__':
    asyncio.run(main(app))