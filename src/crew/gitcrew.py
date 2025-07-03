#!/usr/bin/env python3
"""
GitCrew - AI HR System for GitHub Developer Analysis
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from src.crew.tools.github import GitHubProfileAnalyzer

# Load environment variables
load_dotenv()

@CrewBase
class GitCrew:
    """AI HR System for analyzing GitHub developers using CrewAI"""
    
    def __init__(self):
        """Initialize GitCrew with GitHub tools and configuration"""
        # Initialize LLM
        self.llm = LLM(model="gemini/gemini-2.0-flash")
        
        # Initialize tools
        self.github_analyzer = GitHubProfileAnalyzer()
        
        # Load configuration
        self.config_path = Path(__file__).parent / "config"
        
        # Load YAML configurations
        self.agents_config = self._load_yaml_config("agents.yaml")
        self.tasks_config = self._load_yaml_config("tasks.yaml")
    
    def _load_yaml_config(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file"""
        config_file = self.config_path / filename
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}
    
    @agent
    def github_data_collector(self) -> Agent:
        """GitHub Data Collection Specialist Agent"""
        return Agent(
            config=self.agents_config.get('github_data_collector', {}),
            verbose=True,
            tools=[self.github_analyzer],
            llm=self.llm
        )
    
    @agent
    def skill_assessment_analyst(self) -> Agent:
        """Developer Skill Assessment Analyst Agent"""
        return Agent(
            config=self.agents_config.get('skill_assessment_analyst', {}),
            verbose=True,
            tools=[],
            llm=self.llm
        )
    
    @agent
    def technical_profiler(self) -> Agent:
        """Technical Profile Specialist Agent"""
        return Agent(
            config=self.agents_config.get('technical_profiler', {}),
            verbose=True,
            tools=[],
            llm=self.llm
        )
    
    @agent
    def report_generator(self) -> Agent:
        """Technical Report Writer Agent"""
        return Agent(
            config=self.agents_config.get('report_generator', {}),
            verbose=True,
            tools=[],
            llm=self.llm
        )
    
    @task
    def collect_github_data(self) -> Task:
        """GitHub Data Collection Task"""
        return Task(
            config=self.tasks_config.get('collect_github_data', {}),
            agent=self.github_data_collector()
        )
    
    @task
    def assess_developer_skills(self) -> Task:
        """Developer Skills Assessment Task"""
        return Task(
            config=self.tasks_config.get('assess_developer_skills', {}),
            agent=self.skill_assessment_analyst()
        )
    
    @task
    def create_technical_profile(self) -> Task:
        """Technical Profile Creation Task"""
        return Task(
            config=self.tasks_config.get('create_technical_profile', {}),
            agent=self.technical_profiler()
        )
    
    @task
    def generate_analysis_report(self) -> Task:
        """Analysis Report Generation Task"""
        return Task(
            config=self.tasks_config.get('generate_analysis_report', {}),
            agent=self.report_generator()
        )
    
    @crew
    def crew(self) -> Crew:
        """Create and configure the crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )