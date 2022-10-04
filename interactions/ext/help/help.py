from datetime import datetime

from interactions import (
    Client,
    Command,
    Embed,
    EmbedField,
    EmbedFooter,
    Extension,
    OptionType,
    Permissions,
    extension_command,
)

class Help(Extension):
    global name, description, default_member_permissions

    def __init__(
        self,
        client,
        embed_title,
        embed_description,
        embed_color,
        embed_footer,
        embed_timestamp,
        ephemeral,
        subcommands,
    ):
        self.client: Client = client
        self.embed_title: str = embed_title
        self.embed_description: str = embed_description
        self.embed_color: int = embed_color
        self.embed_footer: EmbedFooter = embed_footer
        self.embed_timestamp: bool = embed_timestamp
        self.ephemeral: bool = ephemeral
        self.subcommands: bool = subcommands

        self.allCommands: list = []
        self.embed: Embed = None

    def parse_value(self, cmd: Command):
        value = ""
        # have options
        if cmd.options:
            # have subcommands
            if cmd.has_subcommands:
                value += f"`{cmd.name}`\n"
                # have subcommand groups
                if (
                    len(
                        groups := [
                            i
                            for i in cmd.options
                            if i.type == OptionType.SUB_COMMAND_GROUP
                        ]
                    )
                    > 0
                ):
                    groups.sort(key=lambda x: x.name)
                    for group in groups:
                        value += f"┣ `{group.name}`\n"
                        # subcommands in group
                        for sub in group.options:
                            # subcommand in group has options
                            if sub.options:
                                sub.options.sort(key=lambda x: x.required)
                                value += f"┃ ┣ `{sub.name}{''.join([f' <{i.name}>' if i.required else f' [{i.name}]' for i in sub.options])}`{f' - {sub.description}' if sub.description != 'No description set' else ''}\n"
                            # subcommand has no options
                            else:
                                value += f"┃ ┣ `{sub.name}`{f' - {sub.description}' if sub.description != 'No description set' else ''}\n"
                # process subcommands without groups
                for subcommand in cmd.options:
                    if subcommand.type == OptionType.SUB_COMMAND:
                        # subcommand has options
                        if subcommand.options:
                            subcommand.options.sort(key=lambda x: x.required)
                            value += f"┣ `{subcommand.name}{''.join([f' <{i.name}>' if i.required else f' [{i.name}]' for i in subcommand.options])}`{f' - {subcommand.description}' if subcommand.description != 'No description set' else ''}\n"
                        # subcommand has no options
                        else:
                            value += f"┣ `{subcommand.name}`{f' - {subcommand.description}' if subcommand.description != 'No description set' else ''}\n"
            # no subcommands
            else:
                cmd.options.sort(key=lambda x: x.required)
                value += f"`{cmd.name}{''.join([f' <{i.name}>' if i.required else f' [{i.name}]' for i in cmd.options])}`{f' - {cmd.description}' if cmd.description != 'No description set' else ''}\n"
        # don't have options
        else:
            value += f"`{cmd.name}`{f' - {cmd.description}' if cmd.description != 'No description set' else ''}\n"
        return value

    @extension_command(
        name='help',
        description='Shows help message',
        default_member_permissions=Permissions.DEFAULT,
    )
    async def _help(self, ctx):
        if (
            not self.allCommands
            or self.allCommands != self.client._commands
            or self.embed is None
        ):
            self.allCommands = self.client._commands
            commands = {i.name: i for i in self.allCommands.copy()}
            extensions = []
            for i in self.client._extensions.values():
                if isinstance(i, Extension) and not i.__module__.startswith(
                    "interactions.ext."
                ):
                    extensions.append(i)
            extensions.sort(key=lambda x: x.__module__)

            fields = []
            for ext in extensions:
                value = ""
                for command in ext._commands:
                    cmd = commands[command[8:]]
                    if self.subcommands:
                        value += self.parse_value(cmd)
                    else:
                        value += f"`{cmd.name}`{f' - {cmd.description}' if cmd.description != 'No description set' else ''}\n"
                    commands.pop(command[8:])
                if value:
                    fields.append(
                        EmbedField(
                            name=ext.__class__.__name__, value=value, inline=False
                        )
                    )
            if commands:
                value = ""
                for cmd in commands.values():
                    if self.subcommands:
                        value += self.parse_value(cmd)
                    else:
                        value += f"`{cmd.name}`{f' - {cmd.description}' if cmd.description != 'No description set' else ''}\n"
                if value:
                    fields.append(
                        EmbedField(name="No category", value=value, inline=False)
                    )

            self.embed = Embed(
                title=self.embed_title,
                description=self.embed_description,
                color=self.embed_color,
                fields=fields,
                footer=self.embed_footer,
                timestamp=datetime.utcnow() if self.embed_timestamp else None,
            )
        await ctx.send(embeds=[self.embed], ephemeral=self.ephemeral)


def setup(
    client,
    embed_title="Help",  # Title of the embed
    embed_description="Here is a list of all commands",  # Description of the embed
    embed_color=0x000000,  # Color of the embed
    embed_footer=None,  # Footer of the embed
    embed_timestamp=False,  # Weather to add timestamp to the embed
    ephemeral=False,  # Whether the response is ephemeral
    subcommands=True,  # Whether to show subcommands
):
    return Help(
        client,
        embed_title,
        embed_description,
        embed_color,
        embed_footer,
        embed_timestamp,
        ephemeral,
        subcommands,
    )
