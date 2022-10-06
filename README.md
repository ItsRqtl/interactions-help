# interactions-help

[![ipy](https://img.shields.io/badge/using-interactions.py-000000.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/interactions-py/library)

WIP: This extension is currently work-in-progress, which means it might not function well.

## Installation

### Install from PyPi

```bat
pip install -U interactions-help
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
client.load("interactions.ext.help", embed_color=0x00FF00, ephemeral=True, subcommands=True)
```

### Pagination

Do you have a long list of commands? Now you can paginate it with [dinteractions-paginator](https://github.com/interactions-py/paginator)!
To paginate the help command, put `pagination=True` when you load the extension.

```py
client.load("interactions.ext.help", pagination=True)
```

To customize the paginator, do the following:

```py
from interactions.ext.help import PaginatorFormat
...
client.load("interactions.ext.help", pagination=True, paginator_format=PaginatorFormat(...))
```

PaginatorFormat has exactly the same params as [Paginator](https://github.com/interactions-py/paginator#-class-paginator) except:

- it does not take `func_before_edit` and `func_after_edit`
- `use_select` is forced to be False (the title is the same across pages)
- `client` and `ctx` will be applied itself

### Parameters for client.load

|Parameter|Type|Description|Default value|
|---|---|---|---|
|consider_scope|Optional[bool]|Only show commands that is available in guild|True|
|consider_permissions|Optional[bool]|Only show commands that the user can use|True|
|embed_title|Optional[str]|Title of the embed|Help|
|embed_description|Optional[str]|Description of the embed|Here is a list of all commands|
|embed_color|Optional[int]|Color of the embed|0x000000|
|embed_footer|Optional[EmbedFooter]|Footer of the embed|None|
|embed_timestamp|Optional[bool]|Whether to add a timestamp to the embed|False|
|ephemeral|Optional[bool]|Whether the response is ephemeral (ignored if pagination is enabled)|False|
|subcommands|Optional[bool]|Whether to show subcommands|True|
|ignore_class|Optional[List[str]]|List of names of extension class to ignore|[]|
|ignore_command|Optional[list[str]]|List of names of commands to ignore|[]|
|pagination|Optional[bool]|Whether to paginate the help command|False|
|paginator_format|Optional[PaginatorFormat]|Format of the paginator (ignored if pagination is disabled)|PaginatorFormat()|
|no_category|Optional[str]|Name of the category for commands with no category (not in a class)|No category|
