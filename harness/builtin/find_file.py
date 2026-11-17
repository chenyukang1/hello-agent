from harness.tools import Tool

FIND_FILE_SCHMEA = (
    {
        "type": "object",
        "properties": {
            "file_name": {
                "type": "string",
                "description": "Path of the file to read",
            }
        },
        "required": ["file_name"],
        "additionalProperties": False,
    },
)


def find_file_tool(args):
    """find files"""

    def find_file(file_name):
        """find file"""
        return "hello, agent"

    return Tool(
        "FindFile",
        run=find_file,
        description="Obtain the content of file.",
        input_schema={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Path of the file to read",
                }
            },
            "required": ["file_name"],
            "additionalProperties": False,
        },
        is_read_only=True,
    )
