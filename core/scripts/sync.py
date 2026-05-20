#!/usr/bin/env python3
"""
VoiceOps Sync Utility
Synchronizes n8n workflows and ElevenLabs agents to local template definitions.
Usage: python3 sync.py --n8n-id <workflow_id> --el-id <agent_id> --output <template_dir>
"""

import os
import json
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)


class N8NSyncClient:
    """Manages n8n workflow synchronization."""

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json"
        }

    def fetch_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Fetch a workflow definition from n8n."""
        url = f"{self.api_url}/api/v1/workflows/{workflow_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def strip_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove user-specific metadata while preserving node-level
        authentication and credential references.
        """
        stripped = {
            "nodes": workflow.get("nodes", []),
            "connections": workflow.get("connections", {}),
            "pinData": workflow.get("pinData", {}),
        }

        # Preserve meta but strip instance-specific IDs
        meta = workflow.get("meta", {})
        if "instanceId" in meta:
            # Keep instanceId structure but it will be regenerated on import
            pass

        return stripped

    def save_workflow(self, workflow: Dict[str, Any], output_path: str):
        """Save workflow to JSON file with pretty-printing."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(workflow, f, indent=2)
        print(f"✓ Workflow saved to {output_path}")


class ElevenLabsSyncClient:
    """Manages ElevenLabs agent synchronization."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }

    def fetch_agent(self, agent_id: str) -> Dict[str, Any]:
        """Fetch an agent definition from ElevenLabs."""
        url = f"{self.base_url}/conversational_ai/agents/{agent_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def extract_prompt(self, agent: Dict[str, Any]) -> str:
        """Extract system prompt from agent config."""
        return agent.get("system_prompt", "")

    def extract_config(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Extract configuration (non-prompt) from agent."""
        config = {
            "name": agent.get("name", "[AGENT_NAME]"),
            "model": agent.get("model", "gpt-4-turbo"),
            "voice": {
                "voiceId": agent.get("voice_id", "[VOICE_ID]"),
                "stability": agent.get("voice_stability", 0.75),
                "similarityBoost": agent.get("voice_similarity_boost", 0.85)
            },
            "temperature": agent.get("temperature", 0.7),
            "maxTokens": agent.get("max_tokens", 1024),
            "tools": agent.get("tools", [])
        }
        return config

    def save_prompt(self, prompt: str, output_path: str):
        """Save system prompt to text file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(prompt)
        print(f"✓ Prompt saved to {output_path}")

    def save_config(self, config: Dict[str, Any], output_path: str):
        """Save agent config to JSON file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Config saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Sync n8n workflows and ElevenLabs agents to local templates"
    )
    parser.add_argument(
        "--n8n-id",
        help="n8n workflow ID to sync"
    )
    parser.add_argument(
        "--el-id",
        help="ElevenLabs agent ID to sync"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for template files"
    )

    args = parser.parse_args()

    # Load credentials from environment variables
    n8n_url = os.getenv("N8N_API_URL")
    n8n_key = os.getenv("N8N_API_KEY")
    el_key = os.getenv("ELEVENLABS_API_KEY")

    if not n8n_url or not n8n_key:
        print("Error: N8N_API_URL and N8N_API_KEY environment variables required")
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sync n8n workflow
    if args.n8n_id:
        print(f"\nSyncing n8n workflow: {args.n8n_id}")
        try:
            n8n = N8NSyncClient(n8n_url, n8n_key)
            workflow = n8n.fetch_workflow(args.n8n_id)
            stripped = n8n.strip_workflow(workflow)
            n8n.save_workflow(stripped, str(output_dir / "workflow.json"))
        except Exception as e:
            print(f"✗ n8n sync failed: {e}")
            sys.exit(1)

    # Sync ElevenLabs agent
    if args.el_id:
        if not el_key:
            print("Warning: ELEVENLABS_API_KEY not set; skipping ElevenLabs sync")
        else:
            print(f"\nSyncing ElevenLabs agent: {args.el_id}")
            try:
                el = ElevenLabsSyncClient(el_key)
                agent = el.fetch_agent(args.el_id)
                prompt = el.extract_prompt(agent)
                config = el.extract_config(agent)
                el.save_prompt(prompt, str(output_dir / "base_agent.txt"))
                el.save_config(config, str(output_dir / "agent_config.json"))
            except Exception as e:
                print(f"✗ ElevenLabs sync failed: {e}")
                sys.exit(1)

    print(f"\n✓ Sync complete. Files written to {output_dir}")


if __name__ == "__main__":
    main()
