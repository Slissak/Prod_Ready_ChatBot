# 🤖 AI Career Assistant - Production Ready Chatbot

## 🌐 **Live Application**

**🎯 Try it now: [AI Career Assistant Chatbot](https://appreadychatbot-dnn8kn3icvh76ztnelzij4.streamlit.app/)**

*This is a fully functional, production-ready chatbot. No setup required - just start chatting!*

## 📋 **Overview & Purpose**

This is a **100% production-ready, fully cloud-deployed AI career assistant chatbot** that helps candidates explore job opportunities and schedule interviews. **Everything runs online - no local setup required.**

### 🎯 **Key Features**
- **Intelligent Job Role Matching**: AI-powered role identification and information retrieval
- **Interactive Chat Interface**: Natural conversation flow with context awareness
- **Automated Interview Scheduling**: Real-time availability checking and booking
- **RAG-Powered Responses**: Detailed job descriptions and requirements from company documents
- **Session Management**: Persistent conversation state across interactions
- **Production Monitoring**: Comprehensive logging and health checks

### 🚀 **Production Status**
- ✅ **Backend**: Running on Azure Container Instances
- ✅ **Frontend**: Deployed on Streamlit Cloud
- ✅ **Database**: PostgreSQL on Supabase
- ✅ **Vector Database**: Pinecone for RAG
- ✅ **AI Model**: OpenAI GPT-4o
- ✅ **Environment**: Fully containerized and scalable

---

## 🏗️ **Architecture Overview**

### **System Components**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│  (Streamlit)    │◄──►│  (Azure +       │◄──►│   Services      │
│                 │    │   LangGraph)    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │    Pinecone     │
                       │   (Supabase)    │    │   (RAG Index)   │
                       └─────────────────┘    └─────────────────┘
```

---

## 🔧 **Backend Architecture - LangGraph Workflow**

The backend is built using **LangGraph**, a framework for building stateful, multi-turn applications with LLMs. The conversation flow is managed through a sophisticated graph-based workflow.

### **LangGraph Workflow Design**

```
┌─────────────┐
│   START     │
└─────┬───────┘
      │
      ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   ROUTER    │────►│  RAG SYSTEM │────►│     END     │
│             │     │             │     │             │
│ • Analyzes  │     │ • Retrieves │     │ • Returns   │
│   user      │     │   job docs  │     │   response  │
│   intent    │     │ • Generates │     │ • Updates   │
│ • Extracts  │     │   answers   │     │   session   │
│   job role  │     │ • Offers    │     │             │
│ • Routes    │     │   scheduling│     │             │
│   to next   │     │             │     │             │
│   node      │     │             │     │             │
└─────┬───────┘     └─────────────┘     └─────────────┘
      │
      ▼
┌─────────────┐     ┌─────────────┐
│ SQL DATABASE│────►│     END     │
│             │     │             │
│ • Checks    │     │ • Returns   │
│   available │     │   response  │
│   slots     │     │ • Updates   │
│ • Books     │     │   session   │
│   interviews│     │             │
│ • Updates   │     │             │
│   database  │     │             │
└─────────────┘     └─────────────┘
```

### **Workflow Nodes**

#### **1. Router Node** 🧭
- **Purpose**: Intelligent conversation routing and job role extraction
- **Function**: Analyzes user intent and routes to appropriate service
- **Output**: Next node decision + extracted job role ID

#### **2. RAG System Node** 📚
- **Purpose**: Retrieval-Augmented Generation for job information
- **Function**: Queries Pinecone for relevant job descriptions
- **Output**: Detailed role information + scheduling offer

#### **3. SQL Database Node** 🗄️
- **Purpose**: Interview scheduling and availability management
- **Function**: Queries Supabase for available time slots
- **Output**: Available slots + booking confirmation

#### **4. End Conversation Node** 🏁
- **Purpose**: Graceful conversation termination
- **Function**: Handles sign-offs and session cleanup
- **Output**: Final response + session restart signal

### **State Management**
The system maintains conversation state including:
- `conversation_history`: Chat message history
- `current_job_role`: Active job role context
- `booking_status`: Interview booking state
- `session_id`: Unique session identifier

---

## 🌐 **Deployment Architecture**

### **Backend - Azure Container Instances**
- **Container**: `regprodreadychatbot.azurecr.io/chatbot-backend-wlogs:latestv2`
- **URL**: `http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000`
- **Resources**: 1 CPU, 1.5GB RAM
- **Environment**: Production with secure environment variables

### **Frontend - Streamlit Cloud**
- **Platform**: Streamlit Cloud
- **Repository**: GitHub integration
- **Environment**: Production configuration
- **Features**: Auto-scaling, SSL, CDN

### **Database - Supabase PostgreSQL**
- **Purpose**: Interview slot management
- **Tables**: Available time slots, bookings
- **Features**: Real-time queries, connection pooling
- **Security**: Row-level security, encrypted connections

### **Vector Database - Pinecone**
- **Purpose**: RAG solution for job descriptions
- **Index**: `job-description-index`
- **Content**: Job description PDFs, requirements, responsibilities
- **Features**: Semantic search, metadata filtering

---

## 🔗 **Service Integration**

### **OpenAI Integration**
- **Model**: GPT-4o
- **Usage**: Conversation routing, response generation
- **Features**: Structured output, context awareness

### **Pinecone RAG Solution**
- **Index**: Job description documents
- **Query**: Semantic search for role-specific information
- **Response**: Contextual answers based on company documents

### **Supabase Database**
- **Function**: Interview availability management
- **Operations**: Query open slots, book interviews
- **Real-time**: Live availability updates

---

## 🚀 **Quick Start**

### **For Users**
1. **Access**: Visit the Streamlit Cloud URL
2. **Chat**: Start a conversation about job roles
3. **Explore**: Ask questions about specific positions
4. **Schedule**: Book interviews when ready

### **For Developers**
```bash
# Clone repository
git clone https://github.com/Slissak/Prod_Ready_ChatBot.git
cd Prod_Ready_ChatBot

# Backend (Azure deployed)
curl http://myapp-prodreadychatbot.eastus.azurecontainer.io:8000/health

# Frontend (Streamlit Cloud)
# Visit the deployed Streamlit app
```

---

## 🔧 **Technology Stack**

### **Backend**
- **Framework**: FastAPI + LangGraph
- **AI**: OpenAI GPT-4o
- **Database**: PostgreSQL (Supabase)
- **Vector DB**: Pinecone
- **Container**: Docker + Azure Container Instances
- **Language**: Python 3.12

### **Frontend**
- **Framework**: Streamlit
- **Deployment**: Streamlit Cloud
- **Configuration**: Environment-aware secrets
- **Features**: Session management, real-time chat

### **Infrastructure**
- **Cloud**: Azure (Backend) + Streamlit Cloud (Frontend)
- **Database**: Supabase (PostgreSQL)
- **Vector Search**: Pinecone
- **Monitoring**: Azure Logs + Streamlit Analytics

---

## 📊 **Production Features**

### **Health Monitoring**
- **Health Endpoint**: `/health` - System status
- **Environment Test**: `/env-test` - Configuration validation
- **Logging**: Comprehensive error tracking
- **Metrics**: Response times, success rates

### **Security**
- **Environment Variables**: Secure configuration management
- **CORS**: Cross-origin request handling
- **Input Validation**: Pydantic models
- **Error Handling**: Graceful failure management

### **Scalability**
- **Container Orchestration**: Azure Container Instances
- **Auto-scaling**: Streamlit Cloud
- **Connection Pooling**: Database optimization
- **Caching**: Vector search optimization

---

## 🎯 **Use Cases**

### **For Candidates**
- **Role Exploration**: Learn about available positions
- **Requirements Check**: Understand job requirements
- **Interview Scheduling**: Book convenient time slots
- **Company Information**: Get detailed role descriptions

### **For Recruiters**
- **Automated Screening**: Initial candidate engagement
- **Availability Management**: Real-time slot booking
- **Information Distribution**: Consistent role information
- **Lead Generation**: Qualified candidate collection

---

## 🔮 **Future Enhancements**

### **Planned Features**
- **Multi-language Support**: International candidate support
- **Advanced Analytics**: Conversation insights and metrics
- **Integration APIs**: HR system connectivity
- **Mobile Optimization**: Enhanced mobile experience

### **Scalability Plans**
- **Multi-region Deployment**: Global availability
- **Advanced Caching**: Redis integration
- **Microservices**: Service decomposition
- **Event-driven Architecture**: Real-time updates

---

## 📞 **Support & Contact**

### **Technical Support**
- **Issues**: GitHub Issues
- **Documentation**: This README
- **Deployment**: Azure + Streamlit Cloud dashboards

### **Production Status**
- **Backend**: ✅ Running on Azure
- **Frontend**: ✅ Deployed on Streamlit Cloud
- **Database**: ✅ Active on Supabase
- **Vector DB**: ✅ Operational on Pinecone

---

## 👨‍💻 **Author**

**Sivan Lissak** - Full-stack developer and AI enthusiast

*This entire production-ready chatbot system was built by Sivan Lissak with the help of helpful AI assistants. From the initial concept to the final deployment, every component has been carefully crafted to create a seamless, professional experience.*

## 📄 **License**

This project is proprietary and confidential. All rights reserved.

---

**🎉 Production Ready - No Local Setup Required!**
