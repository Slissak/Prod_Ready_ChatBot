# 🚀 Environment Variable Validation Plan

## 🎯 **Goal**
Verify API keys and environment variables are being used properly across all deployment scenarios:
1. Local development with `.env` file
2. Local Docker container
3. Azure Container Instance

## 📋 **Phase 1: Enhanced Logging & Health Checks** ✅ COMPLETED

### ✅ **What Was Implemented:**

1. **Enhanced `main.py`**:
   - Added comprehensive logging with emojis for readability
   - Added environment variable validation on startup
   - Added `/health` endpoint with environment variable status
   - Added `/env-test` endpoint for debugging
   - Added startup event logging
   - Enhanced error logging with tracebacks

2. **New Test Scripts**:
   - `test_environment_validation.py` - Comprehensive endpoint testing
   - `test_docker_environment.py` - Docker container testing

### ✅ **Key Features Added:**

```python
# Environment validation on startup
def validate_environment_variables():
    required_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "PINECONE_INDEX_NAME": os.getenv("PINECONE_INDEX_NAME")
    }
    # Validates and logs presence (not values) for security

# Enhanced health endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if all_env_vars_present else "unhealthy",
        "environment_variables": env_status,
        "timestamp": str(uuid4()),
        "version": "1.0.0"
    }
```

## 🧪 **Phase 2: Testing Scenarios**

### **Scenario 1: Local Development (.env file)**

**Steps:**
1. Ensure `.env` file exists in `backend/` directory
2. Start backend server:
   ```bash
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Run validation test:
   ```bash
   python test_environment_validation.py
   ```
4. Check logs for:
   - ✅ Environment variables loaded successfully
   - ✅ All services initialized
   - ✅ Health endpoint returns "healthy"

**Expected Logs:**
```
🚀 FastAPI application starting up...
✅ Environment variables loaded successfully:
   OPENAI_API_KEY: ✅ Present
   DATABASE_URL: ✅ Present
   PINECONE_API_KEY: ✅ Present
   PINECONE_INDEX_NAME: ✅ Present
🚀 Environment validation completed successfully
✅ Application startup completed
```

### **Scenario 2: Local Docker Container**

**Steps:**
1. Build and test Docker container:
   ```bash
   cd backend
   python test_docker_environment.py
   ```
2. Manual Docker test:
   ```bash
   # Build image
   docker build -t chatbot-backend-test .
   
   # Run with environment variables
   docker run -p 8000:8000 \
     -e OPENAI_API_KEY=your_key \
     -e DATABASE_URL=your_url \
     -e PINECONE_API_KEY=your_key \
     -e PINECONE_INDEX_NAME=your_index \
     chatbot-backend-test
   ```
3. Test endpoints:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/env-test
   ```

**Expected Results:**
- ✅ Container starts successfully
- ✅ All environment variables present
- ✅ Health endpoint returns "healthy"
- ✅ Chat endpoint works

### **Scenario 3: Azure Container Instance**

**Steps:**
1. Build and push image to Azure Container Registry:
   ```bash
   # Build with Azure tag
   docker build -t regprodreadychatbot.azurecr.io/chatbot-backend:latest .
   
   # Push to Azure
   docker push regprodreadychatbot.azurecr.io/chatbot-backend:latest
   ```

2. Create Azure Container Instance with secure environment variables:
   ```bash
   az container create \
     --resource-group your-rg \
     --name chatbot-backend \
     --image regprodreadychatbot.azurecr.io/chatbot-backend:latest \
     --ports 8000 \
     --secure-environment-variables \
       OPENAI_API_KEY=your_key \
       DATABASE_URL=your_url \
       PINECONE_API_KEY=your_key \
       PINECONE_INDEX_NAME=your_index
   ```

3. Test Azure deployment:
   ```bash
   # Get container IP
   az container show --resource-group your-rg --name chatbot-backend --query ipAddress.ip --output tsv
   
   # Test endpoints
   curl http://YOUR_AZURE_IP:8000/health
   curl http://YOUR_AZURE_IP:8000/env-test
   ```

## 🔍 **Phase 3: Verification Checklist**

### **✅ Environment Variables**
- [ ] `OPENAI_API_KEY` - Present and valid
- [ ] `DATABASE_URL` - Present and valid PostgreSQL connection
- [ ] `PINECONE_API_KEY` - Present and valid
- [ ] `PINECONE_INDEX_NAME` - Present and valid

### **✅ Health Endpoints**
- [ ] `/health` returns status "healthy"
- [ ] `/env-test` shows all variables present
- [ ] `/` returns API status
- [ ] `/chat` processes messages successfully

### **✅ Logging**
- [ ] Startup logs show environment validation
- [ ] Health check logs are readable
- [ ] Error logs include tracebacks
- [ ] Azure logs are accessible via `az container logs`

### **✅ Security**
- [ ] Environment variable values are NOT logged
- [ ] Only presence/absence is logged
- [ ] Azure secure environment variables are masked

## 🐛 **Phase 4: Troubleshooting**

### **Common Issues & Solutions:**

1. **Missing Environment Variables**
   ```
   ❌ MISSING ENVIRONMENT VARIABLES: ['OPENAI_API_KEY', 'DATABASE_URL']
   ```
   **Solution:** Ensure all variables are set in `.env` file or passed to container

2. **Container CrashLoopBackOff**
   ```
   💥 Environment validation failed: Missing required environment variables
   ```
   **Solution:** Check Azure secure environment variables are properly set

3. **Port Binding Issues**
   ```
   ❌ Health check error: Connection refused
   ```
   **Solution:** Ensure container exposes port 8000 and host binding is correct

4. **Service Initialization Failures**
   ```
   ❌ Failed to initialize OpenAI client: Invalid API key
   ```
   **Solution:** Verify API keys are valid and have proper permissions

## 📊 **Phase 5: Monitoring & Alerts**

### **Azure Log Analytics Query:**
```kusto
ContainerInstanceLog_CL
| where ContainerName_s == "chatbot-backend"
| where Log_s contains "❌" or Log_s contains "💥"
| project TimeGenerated, Log_s
| order by TimeGenerated desc
```

### **Health Check Monitoring:**
```bash
# Set up periodic health checks
while true; do
  curl -f http://YOUR_AZURE_IP:8000/health || echo "Health check failed"
  sleep 60
done
```

## 🎯 **Success Criteria**

### **✅ All Scenarios Must Pass:**
1. **Local Development**: All endpoints respond correctly
2. **Local Docker**: Container starts and all tests pass
3. **Azure Container**: Deploys successfully and responds to requests

### **✅ Logging Requirements:**
- Environment variables validated on startup
- Health checks return detailed status
- Errors include full tracebacks
- Azure logs are readable and searchable

### **✅ Security Requirements:**
- No sensitive data in logs
- Environment variables properly masked in Azure
- Secure environment variables used in production

## 🚀 **Next Steps**

1. **Run Local Tests**:
   ```bash
   cd backend
   python test_environment_validation.py
   ```

2. **Test Docker Locally**:
   ```bash
   cd backend
   python test_docker_environment.py
   ```

3. **Deploy to Azure**:
   - Build and push image
   - Create container instance with secure environment variables
   - Test all endpoints

4. **Monitor & Validate**:
   - Check Azure logs for any errors
   - Verify all endpoints respond correctly
   - Confirm environment variables are properly loaded

---

**📝 Notes:**
- All logs use emojis for better readability in Azure logs
- Environment variable values are never logged for security
- Health endpoints provide detailed status without exposing sensitive data
- Test scripts can be run independently for each deployment scenario
