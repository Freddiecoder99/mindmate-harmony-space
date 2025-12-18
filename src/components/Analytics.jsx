import { useState, useEffect } from 'react';
import { LineChart, Line, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Analytics.css';

const API_URL = 'http://localhost:5000/api';

function Analytics() {
  const [moodData, setMoodData] = useState([]);
  const [stats, setStats] = useState({
    averageMood: 0,
    totalEntries: 0,
    streak: 0,
    trend: 'stable'
  });
  const [emotionBreakdown, setEmotionBreakdown] = useState([]);
  const [triggerFrequency, setTriggerFrequency] = useState([]);
  const [weeklyTrend, setWeeklyTrend] = useState([]);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = () => {
    // Get data from localStorage (conversations)
    const savedConversations = localStorage.getItem('mindmate_conversations');
    
    if (!savedConversations) {
      return;
    }

    const conversations = JSON.parse(savedConversations);
    
    // Extract all messages with emotions
    const allMessages = [];
    conversations.forEach(conv => {
      conv.messages.forEach(msg => {
        if (msg.role === 'user' && msg.emotion) {
          allMessages.push({
            date: new Date(msg.timestamp).toLocaleDateString(),
            emotion: msg.emotion,
            intensity: msg.intensity,
            triggers: msg.triggers || [],
            timestamp: msg.timestamp
          });
        }
      });
    });

    if (allMessages.length === 0) {
      return;
    }

    // Calculate statistics
    calculateStats(allMessages);
    calculateEmotionBreakdown(allMessages);
    calculateTriggerFrequency(allMessages);
    calculateWeeklyTrend(allMessages);
  };

  const calculateStats = (messages) => {
    const totalIntensity = messages.reduce((sum, msg) => sum + msg.intensity, 0);
    const avgMood = totalIntensity / messages.length;
    
    // Calculate streak (consecutive days with entries)
    const uniqueDates = [...new Set(messages.map(m => m.date))].sort();
    let streak = 0;
    const today = new Date().toLocaleDateString();
    
    if (uniqueDates.includes(today)) {
      streak = 1;
      for (let i = uniqueDates.length - 2; i >= 0; i--) {
        const date1 = new Date(uniqueDates[i]);
        const date2 = new Date(uniqueDates[i + 1]);
        const diffDays = Math.floor((date2 - date1) / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
          streak++;
        } else {
          break;
        }
      }
    }

    // Calculate trend (last 3 vs previous 3)
    let trend = 'stable';
    if (messages.length >= 6) {
      const recent = messages.slice(-3);
      const previous = messages.slice(-6, -3);
      
      const recentAvg = recent.reduce((sum, m) => sum + m.intensity, 0) / 3;
      const previousAvg = previous.reduce((sum, m) => sum + m.intensity, 0) / 3;
      
      if (recentAvg > previousAvg + 1) trend = 'improving';
      else if (recentAvg < previousAvg - 1) trend = 'declining';
    }

    setStats({
      averageMood: avgMood.toFixed(1),
      totalEntries: messages.length,
      streak,
      trend
    });
  };

  const calculateEmotionBreakdown = (messages) => {
    const emotionCounts = {};
    
    messages.forEach(msg => {
      emotionCounts[msg.emotion] = (emotionCounts[msg.emotion] || 0) + 1;
    });

    const breakdown = Object.entries(emotionCounts).map(([emotion, count]) => ({
      name: emotion.charAt(0).toUpperCase() + emotion.slice(1),
      value: count,
      percentage: ((count / messages.length) * 100).toFixed(1)
    }));

    setEmotionBreakdown(breakdown);
  };

  const calculateTriggerFrequency = (messages) => {
    const triggerCounts = {};
    
    messages.forEach(msg => {
      msg.triggers.forEach(trigger => {
        triggerCounts[trigger] = (triggerCounts[trigger] || 0) + 1;
      });
    });

    const frequency = Object.entries(triggerCounts)
      .map(([trigger, count]) => ({
        name: trigger.charAt(0).toUpperCase() + trigger.slice(1),
        count
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    setTriggerFrequency(frequency);
  };

  const calculateWeeklyTrend = (messages) => {
    // Group by date and calculate average intensity
    const dateGroups = {};
    
    messages.forEach(msg => {
      if (!dateGroups[msg.date]) {
        dateGroups[msg.date] = [];
      }
      dateGroups[msg.date].push(msg.intensity);
    });

    const trend = Object.entries(dateGroups)
      .map(([date, intensities]) => ({
        date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        mood: (intensities.reduce((a, b) => a + b, 0) / intensities.length).toFixed(1),
        entries: intensities.length
      }))
      .slice(-7); // Last 7 days

    setWeeklyTrend(trend);
  };

  const EMOTION_COLORS = {
    'Happy': '#10b981',
    'Excited': '#f59e0b',
    'Calm': '#06b6d4',
    'Sad': '#3b82f6',
    'Anxious': '#f97316',
    'Angry': '#ef4444',
    'Overwhelmed': '#8b5cf6',
    'Frustrated': '#ec4899',
    'Hopeful': '#14b8a6',
    'Tired': '#6366f1',
    'Confused': '#a855f7',
    'Neutral': '#6b7280'
  };

  const getTrendIcon = () => {
    if (stats.trend === 'improving') return '📈';
    if (stats.trend === 'declining') return '📉';
    return '➡️';
  };

  const getTrendColor = () => {
    if (stats.trend === 'improving') return '#10b981';
    if (stats.trend === 'declining') return '#ef4444';
    return '#6b7280';
  };

  if (stats.totalEntries === 0) {
    return (
      <div className="analytics-empty">
        <div className="empty-icon">📊</div>
        <h3>No Data Yet</h3>
        <p>Start chatting with MindMate to see your emotional insights and trends!</p>
      </div>
    );
  }

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h2>📊 Your Emotional Analytics</h2>
        <p>Insights based on {stats.totalEntries} conversations</p>
      </div>

      {/* Key Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">😊</div>
          <div className="stat-content">
            <div className="stat-label">Average Mood</div>
            <div className="stat-value">{stats.averageMood}<span>/10</span></div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <div className="stat-label">Current Streak</div>
            <div className="stat-value">{stats.streak}<span> days</span></div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">{getTrendIcon()}</div>
          <div className="stat-content">
            <div className="stat-label">Trend</div>
            <div className="stat-value" style={{ color: getTrendColor() }}>
              {stats.trend.charAt(0).toUpperCase() + stats.trend.slice(1)}
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💬</div>
          <div className="stat-content">
            <div className="stat-label">Total Check-ins</div>
            <div className="stat-value">{stats.totalEntries}</div>
          </div>
        </div>
      </div>

      {/* Weekly Mood Trend */}
      {weeklyTrend.length > 0 && (
        <div className="chart-card">
          <h3>📈 7-Day Mood Trend</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={weeklyTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="date" stroke="#6b7280" />
              <YAxis domain={[0, 10]} stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Line 
                type="monotone" 
                dataKey="mood" 
                stroke="#667eea" 
                strokeWidth={3}
                dot={{ fill: '#667eea', r: 5 }}
                activeDot={{ r: 7 }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="chart-note">Higher is better • Track your emotional journey over time</p>
        </div>
      )}

      <div className="charts-row">
        {/* Emotion Breakdown */}
        {emotionBreakdown.length > 0 && (
          <div className="chart-card">
            <h3>🎭 Emotion Breakdown</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={emotionBreakdown}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name} (${entry.percentage}%)`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {emotionBreakdown.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={EMOTION_COLORS[entry.name] || '#6b7280'} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <p className="chart-note">What you've been feeling most</p>
          </div>
        )}

        {/* Trigger Frequency */}
        {triggerFrequency.length > 0 && (
          <div className="chart-card">
            <h3>🎯 Common Triggers</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={triggerFrequency}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="name" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip 
                  contentStyle={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                />
                <Bar dataKey="count" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
            <p className="chart-note">What affects your wellbeing most</p>
          </div>
        )}
      </div>

      {/* Insights */}
      <div className="insights-card">
        <h3>💡 Personalized Insights</h3>
        <div className="insights-list">
          {stats.trend === 'improving' && (
            <div className="insight-item positive">
              <span className="insight-icon">🌟</span>
              <div>
                <strong>Great Progress!</strong>
                <p>Your mood has been trending upward. Keep doing what's working!</p>
              </div>
            </div>
          )}
          
          {stats.trend === 'declining' && (
            <div className="insight-item warning">
              <span className="insight-icon">⚠️</span>
              <div>
                <strong>Check-in Needed</strong>
                <p>Your mood has been lower recently. Consider reaching out to a friend or professional.</p>
              </div>
            </div>
          )}

          {stats.streak >= 3 && (
            <div className="insight-item positive">
              <span className="insight-icon">🔥</span>
              <div>
                <strong>Amazing Streak!</strong>
                <p>You've checked in {stats.streak} days in a row. Consistency builds self-awareness!</p>
              </div>
            </div>
          )}

          {emotionBreakdown.length > 0 && emotionBreakdown[0].value > stats.totalEntries * 0.5 && (
            <div className="insight-item info">
              <span className="insight-icon">🎭</span>
              <div>
                <strong>Dominant Emotion: {emotionBreakdown[0].name}</strong>
                <p>This emotion appears in over 50% of your check-ins. Let's explore what's driving this.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Analytics;
