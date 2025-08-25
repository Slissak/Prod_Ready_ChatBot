# 🚀 Frontend Deployment Guide

## 🏭 **Environment Configuration**

This frontend supports multiple environments with industry-standard configuration management.

### **Environments Supported:**
- **Development** (`development`) - Local development
- **Staging** (`staging`) - Testing environment
- **Production** (`production`) - Live environment

## 🔧 **Configuration Priority**

The application uses this priority order for configuration:

1. **Streamlit Secrets** (highest priority)
2. **Environment Variables**
3. **Environment-specific defaults** (lowest priority)

## 📁 **Configuration Files**

### **Local Development**
```toml
# .streamlit/secrets.toml
BACKEND_URL = "http://localhost:8000"
ENVIRONMENT = "development"
DEBUG = "true"
```

### **Production**
```toml
# .streamlit/secrets.toml (in Streamlit Cloud)
BACKEND_URL = "http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000"
ENVIRONMENT = "production"
DEBUG = "false"
```

## 🚀 **Deployment Options**

### **Option 1: Streamlit Cloud (Recommended)**

1. **Push to GitHub**
2. **Connect to Streamlit Cloud**
3. **Configure secrets in Streamlit Cloud dashboard:**
   ```
   BACKEND_URL = "http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000"
   ENVIRONMENT = "production"
   DEBUG = "false"
   ```

### **Option 2: Azure Container Instances**

1. **Create Dockerfile for frontend**
2. **Build and push image**
3. **Deploy with environment variables:**
   ```bash
   az container create \
     --resource-group prodready-chatbot \
     --name frontend-container \
     --image your-frontend-image \
     --ports 8501 \
     --environment-variables \
       BACKEND_URL=http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000 \
       ENVIRONMENT=production \
       DEBUG=false
   ```

### **Option 3: Local Development**

```bash
# Run locally
cd frontend
streamlit run app.py
```

## 🔍 **Testing Different Environments**

### **Test Local Backend**
```bash
# Ensure backend is running locally
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run frontend
cd frontend
streamlit run app.py
```

### **Test Azure Backend**
```bash
# Update secrets.toml to point to Azure
echo 'BACKEND_URL = "http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000"' > .streamlit/secrets.toml

# Run frontend
streamlit run app.py
```

## 🛠️ **Debug Mode**

When `DEBUG = "true"`, the app shows:
- Current environment
- Backend URL
- Available endpoints
- Configuration details

## 🔐 **Security Notes**

- Never commit sensitive data to version control
- Use Streamlit secrets for production deployments
- Environment variables are automatically masked in logs
- Debug mode should be disabled in production

## 📊 **Health Checks**

The app automatically tests backend connectivity:
- Health endpoint: `/health`
- Environment test: `/env-test`
- Chat endpoint: `/chat`

## 🎯 **Success Criteria**

✅ Frontend connects to backend successfully
✅ Chat functionality works
✅ Session management works
✅ Environment-specific features work
✅ Debug information available when needed
