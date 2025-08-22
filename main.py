from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.crew.gitcrew import GitCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="GitCrew AI HR System API",
    description="AI-powered GitHub developer analysis for HR and recruitment",
    version="1.0.0"
)

# Initialize CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for structured input
class GitHubAnalysisRequest(BaseModel):
    github_username: str

@app.get("/")
async def root():
    return {
        "message": "🚀 Welcome to GitCrew AI HR System API!",
        "description": "AI-powered GitHub developer analysis for recruitment and HR evaluation",
        "version": "1.0.0",
        "features": [
            "GitHub profile comprehensive analysis",
            "Code quality assessment",
            "Skill evaluation and recommendations",
            "Developer experience insights",
            "Recruitment compatibility scoring"
        ]
    }

@app.post("/analyze")
async def analyze_github_profile(request: GitHubAnalysisRequest):
    """
    Analyze GitHub developer profile using AI crew
    """
    try:
        if not request.github_username.strip():
            raise HTTPException(status_code=400, detail="GitHub username is required")
        
        # Create GitCrew instance
        git_crew = GitCrew()
        
        # Prepare inputs for the crew
        inputs = {
            "github_username": request.github_username
        }
        
        # Get the crew and run analysis
        crew = git_crew.crew()
        result = crew.kickoff(inputs=inputs)
        
        return {
            "status": "success",
            "github_username": request.github_username,
            "analysis_steps": [
                "🔍 GitHub profile data extraction",
                "📊 Repository analysis and code evaluation",
                "🎯 Skill assessment and technology stack review",
                "📈 Contribution patterns and activity analysis",
                "🏆 Overall developer evaluation and scoring"
            ],
            "result": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub analysis failed: {str(e)}")
