def authorize_tool(tool_name,allowed_tools,trusted_instruction=False):
 return trusted_instruction and tool_name in allowed_tools
