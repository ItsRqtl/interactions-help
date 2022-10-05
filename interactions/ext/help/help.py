from datetime import datetime
from typing import Dict, List, Optional, Union

from interactions.ext.paginator import Page, Paginator

from interactions import (
    Button,
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


class PaginatorFormat:
    def __init__(
        self,
        timeout: Optional[Union[int, float]] = 60,
        author_only: bool = False,
        use_buttons: bool = True,
        use_index: bool = False,
        extended_buttons: bool = True,
        buttons: Optional[Dict[str, Button]] = None,
        placeholder: str = "Page",
        disable_after_timeout: bool = True,
        remove_after_timeout: bool = False,
    ) -> None:
        self.timeout = timeout
        self.author_only = author_only
        self.use_buttons = use_buttons
        self.use_index = use_index
        self.extended_buttons = extended_buttons
        self.buttons = buttons
        self.placeholder = placeholder
        self.disable_after_timeout = disable_after_timeout
        self.remove_after_timeout = remove_after_timeout


class Help(Extension):
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
        ignore_class,
        ignore_command,
        pagination,
        paginator_format,
    ):
        self.client: Client = client
        self.embed_title: str = embed_title
        self.embed_description: str = embed_description
        self.embed_color: int = embed_color
        self.embed_footer: EmbedFooter = embed_footer
        self.embed_timestamp: bool = embed_timestamp
        self.ephemeral: bool = ephemeral
        self.subcommands: bool = subcommands
        self.ignore_class: List[str] = ignore_class
        self.ignore_command: List[str] = ignore_command
        self.pagination: bool = pagination
        self.paginator_format: PaginatorFormat = paginator_format

        self.allCommands: list = []
        self.embed: Embed = None
        self.paginator: Paginator = None

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
                        groups := [i for i in cmd.options if i.type == OptionType.SUB_COMMAND_GROUP]
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
        name="help",
        description="Shows help message",
        default_member_permissions=Permissions.DEFAULT,
    )
    async def _help(self, ctx):
        if (
            not self.allCommands
            or self.allCommands != self.client._commands
            or (self.embed is None and self.paginator is None)
        ):
            self.allCommands = self.client._commands
            commands = {i.name: i for i in self.allCommands.copy()}
            extensions = []
            for i in self.client._extensions.values():
                if isinstance(i, Extension) and not i.__module__.startswith("interactions.ext."):
                    extensions.append(i)
            extensions.sort(key=lambda x: x.__module__)

            fields = []
            for ext in extensions:
                if ext.__class__.__name__ in self.ignore_class:
                    for command in ext._commands:
                        commands.pop(command[8:])
                else:
                    value = ""
                    for command in ext._commands:
                        if command[8:].lower() not in self.ignore_command:
                            cmd = commands[command[8:]]
                            if self.subcommands:
                                value += self.parse_value(cmd)
                            else:
                                value += f"`{cmd.name}`{f' - {cmd.description}' if cmd.description != 'No description set' else ''}\n"
                        commands.pop(command[8:])
                    if value:
                        fields.append(
                            EmbedField(name=ext.__class__.__name__, value=value, inline=False)
                        )
            if commands:
                for command in commands:
                    if command[8:].lower() not in self.ignore_command:
                        cmd = commands[command[8:]]
                        if self.subcommands:
                            value += self.parse_value(cmd)
                        else:
                            value += f"`{cmd.name}`{f' - {cmd.description}' if cmd.description != 'No description set' else ''}\n"
                if value:
                    fields.append(EmbedField(name="No category", value=value, inline=False))

            if self.pagination and len(fields) > 1:
                self.embed = None
                self.paginator = Paginator(
                    self.client,
                    ctx,
                    [
                        Page(
                            embeds=[
                                Embed(
                                    title=self.embed_title,
                                    description=self.embed_description,
                                    color=self.embed_color,
                                    fields=[i],
                                    footer=self.embed_footer,
                                    timestamp=datetime.utcnow() if self.embed_timestamp else None,
                                )
                            ]
                        )
                        for i in fields
                    ],
                    (pf := self.paginator_format).timeout,
                    pf.author_only,
                    pf.use_buttons,
                    False,
                    pf.use_index,
                    pf.extended_buttons,
                    pf.buttons,
                    pf.placeholder,
                    pf.disable_after_timeout,
                    pf.remove_after_timeout,
                )
            else:
                self.paginator = None
                self.embed = Embed(
                    title=self.embed_title,
                    description=self.embed_description,
                    color=self.embed_color,
                    fields=fields,
                    footer=self.embed_footer,
                    timestamp=datetime.utcnow() if self.embed_timestamp else None,
                )
        if self.embed:
            await ctx.send(
                embeds=[self.embed],
                ephemeral=False if self.pagination else self.ephemeral,
            )
        elif self.paginator:
            self.paginator.ctx = ctx
            await Paginator(**self.paginator._json).run()


def setup(
    client,
    embed_title: Optional[str] = "Help",  # Title of the embed
    embed_description: Optional[str] = "Here is a list of all commands",  # Description of the embed
    embed_color: Optional[int] = 0x000000,  # Color of the embed
    embed_footer: Optional[EmbedFooter] = None,  # Footer of the embed
    embed_timestamp: Optional[bool] = False,  # Weather to add timestamp to the embed
    ephemeral: Optional[
        bool
    ] = False,  # Whether the response is ephemeral (ignored if pagination is enabled)
    subcommands: Optional[bool] = True,  # Whether to show subcommands
    ignore_class: Optional[List[str]] = [],  # List of names of extension class to ignore
    ignore_command: Optional[List[str]] = [],  # List of names of commands to ignore
    pagination: Optional[bool] = False,  # Whether to paginate the embed
    paginator_format: Optional[
        PaginatorFormat
    ] = PaginatorFormat(),  # Format of the paginator (ignored if pagination is disabled)
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
        ignore_class,
        [i.lower() for i in ignore_command],
        pagination,
        paginator_format,
    )
