# interactions-help

WIP: This extension is currently work-in-progress, which means it might not function well.

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

### Default configuration

![image](https://github.com/ItsRqtl/interactions-help/blob/master/img/preview-original.png?raw=true)

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
|embed_title|Optional[str]|Title of the embed|Help|
|embed_description|Optional[str]|Description of the embed|Here is a list of all commands|
|embed_color|Optional[int]|Color of the embed|0x000000|
|embed_footer|Optional[EmbedFooter]|Footer of the embed|None|
|embed_timestamp|Optional[bool]|Whether to add a timestamp to the embed|False|
|ephemeral|Optional[bool]|Whether the response is ephemeral|False|
|subcommands|Optional[bool]|Whether to show subcommands|True|
|ignore_class|Optional[List[str]]|List of names of extension class to ignore|[]|
|ignore_command|Optional[list[str]]|List of names of commands to ignore|[]|
