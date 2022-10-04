# interactions-help

## Installation

### Install from PyPi

```bat
Currently not available
```

### Install from github

```bat
pip install git+https://github.com/ItsRqtl/interactions-help.git
```

### Build from source

```bat
git clone https://github.com/ItsRqtl/interactions-help.git
cd interactions-help
pip install .
```

## Usage

### Loading the extension

```py
from interactions import Client

client = Client(token="...")

client.load("interactions.ext.help")

client.start()
```

### Configurate the help command

To configurate the help command, simply pass the values when you load the extension.

```py
from interactions import Client

client = Client(token="...")

client.load("interactions.ext.help", embed_color=0x00FF00, ephemeral=True, subcommands=True)

client.start()
```

Here is the parameters

|Parameter|Type|Description|Default value|
|---|---|---|---|
|cmd_name|str|The name of the command|help|
|cmd_description|str|The description of the command|Shows help message|
|embed_title|str|Title of the embed|Help|
|embed_description|str|Description of the embed|Here is a list of all commands|
|embed_color|int|Color of the embed|0x000000|
|embed_footer|EmbedFooter|Footer of the embed|None|
|embed_timestamp|bool|Whether to add a timestamp to the embed|False|
|default_member_permissions|Permissions|Default permissions for the command|Permissions.DEFAULT|
|ephemeral|bool|Whether the response is ephemeral|False|
|subcommands|bool|Whether to show subcommands|True|