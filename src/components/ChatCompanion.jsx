import { useState, useEffect, useRef } from 'react';
import './ChatCompanion.css';

const API_URL = 'http://localhost:5000/api';

function ChatCompanion() {
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(null);
  const [currentMessages, setCurrentMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [insights, setInsights] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentMessages]);

  // Initialize with first conversation
  useEffect(() => {
    const savedConversations = localStorage.getItem('mindmate_conversations');
    if (savedConversations) {
      const parsed = JSON.parse(savedConversations);
      setConversations(parsed);
      if (parsed.length > 0) {
        loadConversation(parsed[0].id);
      }
    } else {
      createNewConversation();
    }
    loadInsights();
  }, []);

  // Save conversations to localStorage
  useEffect(() => {
    if (conversations.length > 0) {
      localStorage.setItem('mindmate_conversations', JSON.stringify(conversations));
    }
  }, [conversations]);

  const createNewConversation = () => {
    const newConv = {
      id: Date.now().toString(),
      title: 'New Conversation',
      messages: [],
      created: new Date().toISOString(),
      lastActivity: new Date().toISOString()
    };
    
    setConversations(prev => [newConv, ...prev]);
    setCurrentConversationId(newConv.id);
    setCurrentMessages([]);
  };

  const loadConversation = (convId) => {
    const conv = conversations.find(c => c.id === convId);
    if (conv) {
      setCurrentConversationId(convId);
      setCurrentMessages(conv.messages);
    }
  };

  const updateConversationTitle = (convId, firstMessage) => {
    const title = firstMessage.length > 40 
      ? firstMessage.substring(0, 40) + '...'
      : firstMessage;
    
    setConversations(prev => prev.map(c => 
      c.id === convId ? { ...c, title, lastActivity: new Date().toISOString() } : c
    ));
  };

  const deleteConversation = (convId) => {
    setConversations(prev => {
      const updated = prev.filter(c => c.id !== convId);
      
      if (currentConversationId === convId) {
        if (updated.length > 0) {
          loadConversation(updated[0].id);
        } else {
          createNewConversation();
        }
      }
      
      return updated;
    });
  };

  const loadInsights = async () => {
    try {
      const response = await fetch(`${API_URL}/chat/insights`);
      const data = await response.json();
      setInsights(data);
    } catch (error) {
      console.error('Error loading insights:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentConversationId) return;

    const userMsg = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };
    
    const newMessages = [...currentMessages, userMsg];
    setCurrentMessages(newMessages);
    
    // Update title if first message
    if (currentMessages.length === 0) {
      updateConversationTitle(currentConversationId, inputMessage);
    }
    
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await fetch(`${API_URL}/chat/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: inputMessage,
          conversation_id: currentConversationId
        })
      });

      const data = await response.json();

      if (data.success) {
        const assistantMsg = {
          role: 'assistant',
          content: data.response,
          timestamp: new Date().toISOString(),
          emotion: data.emotion,
          intensity: data.intensity,
          triggers: data.triggers,
          urgency: data.urgency
        };

        const updatedMessages = [...newMessages, assistantMsg];
        setCurrentMessages(updatedMessages);
        
        // Save to conversation
        setConversations(prev => prev.map(c => 
          c.id === currentConversationId 
            ? { ...c, messages: updatedMessages, lastActivity: new Date().toISOString() }
            : c
        ));
        
        // Update insights
        loadInsights();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMsg = {
        role: 'assistant',
        content: '❌ Sorry, I had trouble connecting. Make sure the backend is running!',
        timestamp: new Date().toISOString()
      };
      
      setCurrentMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    e.stopPropagation(); 
    sendMessage();
  }
};

  const getEmotionColor = (emotion) => {
    const colors = {
      happy: '#10b981',
      excited: '#f59e0b',
      calm: '#06b6d4',
      sad: '#3b82f6',
      anxious: '#f97316',
      angry: '#ef4444',
      overwhelmed: '#8b5cf6',
      frustrated: '#ec4899',
      hopeful: '#14b8a6',
      tired: '#6366f1',
      confused: '#a855f7',
      neutral: '#6b7280'
    };
    return colors[emotion?.toLowerCase()] || '#6b7280';
  };

  const currentConv = conversations.find(c => c.id === currentConversationId);

  return (
    <div className="chat-companion-container">
      {/* History Sidebar */}
      <div className={`chat-history-sidebar ${showHistory ? 'show' : ''}`}>
        <div className="history-header">
          <h3>💬 Chat History</h3>
          <button 
            className="new-chat-btn"
            onClick={createNewConversation}
          >
            ➕ New Chat
          </button>
        </div>
        
        <div className="history-list">
          {conversations.length === 0 ? (
            <p className="empty-history">No conversations yet</p>
          ) : (
            conversations.map(conv => (
              <div 
                key={conv.id}
                className={`history-item ${conv.id === currentConversationId ? 'active' : ''}`}
                onClick={() => {
                  loadConversation(conv.id);
                  setShowHistory(false);
                }}
              >
                <div className="history-item-header">
                  <span className="history-title">{conv.title}</span>
                  <button 
                    className="delete-conv-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm('Delete this conversation?')) {
                        deleteConversation(conv.id);
                      }
                    }}
                  >
                    🗑️
                  </button>
                </div>
                <div className="history-meta">
                  <span>{conv.messages.length} messages</span>
                  <span>{new Date(conv.lastActivity).toLocaleDateString()}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Chat */}
      <div className="chat-main">
        <div className="chat-header">
          <button 
            className="history-toggle-btn"
            onClick={() => setShowHistory(!showHistory)}
          >
            ☰
          </button>
          <div className="chat-header-content">
            <div className="chat-avatar">🧠</div>
            <div>
              <h2>MindMate Companion</h2>
              <p className="chat-status">
                <span className="status-dot"></span> Always here for you
              </p>
            </div>
          </div>
          <button 
            className="new-chat-btn-mobile"
            onClick={createNewConversation}
            title="New Conversation"
          >
            ➕
          </button>
        </div>

        <div className="chat-messages">
          {currentMessages.length === 0 ? (
            <div className="chat-welcome">
              <div className="welcome-icon">💬</div>
              <h3>Welcome to your safe space</h3>
              <p>I'm here to listen, support, and help you navigate your emotional journey. 
                 Feel free to share what's on your mind - there's no judgment here, just understanding.</p>
              <div className="welcome-suggestions">
                <p>Try saying:</p>
                <button onClick={() => setInputMessage("I'm feeling stressed today")}>
                  "I'm feeling stressed today"
                </button>
                <button onClick={() => setInputMessage("I need some encouragement")}>
                  "I need some encouragement"
                </button>
                <button onClick={() => setInputMessage("How can I manage anxiety?")}>
                  "How can I manage anxiety?"
                </button>
              </div>
            </div>
          ) : (
            currentMessages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? '👤' : '🧠'}
                </div>
                <div className="message-content">
                  <div className="message-text">{msg.content}</div>
                  {msg.emotion && msg.role === 'user' && (
                    <div className="message-emotion">
                      <span 
                        className="emotion-badge"
                        style={{ backgroundColor: getEmotionColor(msg.emotion) }}
                      >
                        {msg.emotion} ({msg.intensity}/10)
                      </span>
                      {msg.triggers && msg.triggers.length > 0 && (
                        <span className="trigger-badge">
                          🎯 {msg.triggers.join(', ')}
                        </span>
                      )}
                    </div>
                  )}
                  <div className="message-time">
                    {new Date(msg.timestamp).toLocaleTimeString([], { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </div>
                </div>
              </div>
            ))
          )}
          
          {isTyping && (
            <div className="message assistant">
              <div className="message-avatar">🧠</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share what's on your mind..."
            className="chat-input"
            rows="1"
          />
          <button 
            onClick={sendMessage} 
            className="chat-send-btn"
            disabled={!inputMessage.trim() || isTyping}
          >
            {isTyping ? '⏳' : '💬'}
          </button>
        </div>
      </div>

      {/* Insights Sidebar */}
      <div className="chat-insights">
        <h3>📊 Your Journey</h3>
        
        <div className="insight-card">
          <div className="insight-label">Total Conversations</div>
          <div className="insight-value">{conversations.length}</div>
        </div>

        <div className="insight-card">
          <div className="insight-label">Total Messages</div>
          <div className="insight-value">
            {conversations.reduce((sum, c) => sum + c.messages.length, 0)}
          </div>
        </div>

        {insights && insights.total_entries > 0 && (
          <>
            <div className="insight-card">
              <div className="insight-label">Average Mood</div>
              <div className="insight-value">{insights.average_mood}/10</div>
            </div>

            {insights.common_emotions && insights.common_emotions.length > 0 && (
              <div className="insight-card">
                <div className="insight-label">Common Feelings</div>
                <div className="insight-tags">
                  {insights.common_emotions.map((emotion, idx) => (
                    <span 
                      key={idx} 
                      className="insight-tag"
                      style={{ backgroundColor: getEmotionColor(emotion) }}
                    >
                      {emotion}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        <div className="insight-tip">
          <p>💡 <strong>Tip:</strong> Click "New Chat" to start a fresh conversation for different topics or days!</p>
        </div>
      </div>
    </div>
  );
}

export default ChatCompanion;
