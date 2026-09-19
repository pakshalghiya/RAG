import asyncio

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

import gradio as gr # Add this when the time for deployment comes

from llm import create_llm
from shared_tools import web_search_tool, get_job_recommendation, get_resume_data
from system_prompts import SYSTEM_PROMPT_MCP_TOOLS

# `get_job_recommendation` and `get_resume_data` now live on the MCP server
# (mcp_server.py, started separately with `python mcp_server.py`) instead of
# being imported directly from shared_tools.py.
mcp_client = MultiServerMCPClient(
    {
        "job_finding_tools": {
            "url": "http://localhost:8001/mcp",
            "transport": "streamable_http",
        }
    }
)

mcp_tools = asyncio.run(mcp_client.get_tools())
# tools = [web_search_tool, get_job_recommendation, get_resume_data] # For the first run
tools = [web_search_tool, *mcp_tools]

llm = create_llm()

# System prompt is better to be shared with the students on WhatsApp group. But walk them through the thinking first.
SYSTEM_PROMPT = SYSTEM_PROMPT_MCP_TOOLS

job_search_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

def run_agent():
    response = job_search_agent.invoke(
        {"messages": [{"role": "user", "content": "Find me the best jobs based on my resume data"}]}
    )

    print("\n\n\nACTUAL RESPONSE WITH TOOLS\n\n\n", response)

    return response["messages"][-1].content

def deploy_agent():
    with gr.Blocks(title="Career Match Agent") as iface:
        gr.Markdown("## Career Match Agent")
        gr.Markdown("Finds job openings matched to your resume, using live listings and your indexed resume data.")

        find_jobs_btn = gr.Button("Find Jobs", variant="primary")
        output = gr.Textbox(label="Recommended Jobs", lines=20)

        find_jobs_btn.click(fn=run_agent, inputs=None, outputs=output)

    iface.launch()

if __name__ == "__main__":
    # response = run_agent()
    # print("\nCLEAN RESPONSE\n")
    # print(response)

    deploy_agent()
