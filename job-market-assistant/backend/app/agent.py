# ... (previous imports remain the same)

class JobMarketAgent:
    # ... (previous methods remain the same)
    
    async def generate_response(self, user_id: str, message: str) -> str:
        # Retrieve relevant memories
        memories = await self.memory.retrieve_memories(user_id, message)
        context = self._format_memories(memories)
        
        # Check if we should use a tool
        tool_response = await self._check_tools(message)
        if tool_response:
            return tool_response
        
        # Prepare prompt with context
        prompt = self._build_prompt(message, context)
        
        # Generate response
        response = self.llm.generate_content(prompt)
        
        # Store the interaction
        await self.memory.store_memory(
            user_id=user_id,
            content=f"User: {message}\nAssistant: {response.text}",
            metadata={"type": "conversation"}
        )
        
        return response.text
    
    async def _check_tools(self, message: str) -> Optional[str]:
        """Determine if we should use a tool and return the response"""
        tool_mapping = {
            "trend": ("get_job_trends", ["field", "location"]),
            "demand": ("get_skill_demand", ["skill", "location"]),
            "salary": ("get_salary_estimates", ["job_title", "location"]),
            "remote": ("get_remote_jobs", ["limit"])
        }
        
        for keyword, (tool_name, params) in tool_mapping.items():
            if keyword in message.lower():
                try:
                    # Extract parameters from message (simplified)
                    extracted_params = {}
                    if "location" in params:
                        # Simple location extraction - would need NLP in production
                        if " in " in message:
                            extracted_params["location"] = message.split(" in ")[-1].split(" for ")[0].strip()
                    
                    if "field" in params and "field" not in extracted_params:
                        extracted_params["field"] = "technology"  # Default
                    
                    if "skill" in params:
                        extracted_params["skill"] = message.split("demand for ")[-1].split(" in ")[0].strip()
                    
                    if "job_title" in params:
                        extracted_params["job_title"] = message.split("salary for ")[-1].split(" in ")[0].strip()
                    
                    # Call the tool
                    result = await self.use_tool(tool_name, **extracted_params)
                    return self._format_tool_response(tool_name, result)
                except Exception as e:
                    print(f"Tool error: {e}")
                    return None
                
        return None
    
    def _format_tool_response(self, tool_name: str, result: dict) -> str:
        """Format tool response for the user"""
        if tool_name == "get_job_trends":
            trends = result.get("trends", [])[:3]
            return "Current job trends:\n" + "\n".join(
                f"- {t.get('title', '')}: {t.get('link', '')}"
                for t in trends
            )
        
        elif tool_name == "get_skill_demand":
            count = result.get("count", 0)
            jobs = result.get("results", [])[:3]
            response = f"Current demand: {count} jobs found\nSample jobs:\n"
            return response + "\n".join(
                f"- {j.get('title', '')} at {j.get('company', {}).get('display_name', '')}"
                for j in jobs
            )
        
        elif tool_name == "get_salary_estimates":
            data = result.get("data", [])
            if not data:
                return "Salary data not available for this position"
            return "Salary estimates:\n" + "\n".join(
                f"- {d.get('year')}: ${d.get('value')}/year"
                for series in data
                for d in series.get("data", [])
            )
        
        elif tool_name == "get_remote_jobs":
            jobs = result.get("jobs", [])[:3]
            return "Remote job opportunities:\n" + "\n".join(
                f"- {j.get('title', '')} at {j.get('company', {}).get('display_name', '')}"
                for j in jobs
            )
        
        return "I found some information, but couldn't format it properly."