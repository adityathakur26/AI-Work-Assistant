import React, { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
} from "recharts";
import "./App.css";

function App() {
  const [activities, setActivities] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [insights, setInsights] = useState({});
  const [dailySummary, setDailySummary] = useState("");
  const [score, setScore] = useState({});
  const [categorized,setCategorized]=useState([]);
  const [aiInsights,setAiInsights] = useState([]);
  const [focus,setFocus] = useState({});
  const [coach, setCoach] = useState(null);
  const [currentApp, setCurrentApp] = useState({});
  const [liveStatus, setLiveStatus] = useState({});
  const [timelineData, setTimelineData] = useState([]);
  const [question, setQuestion] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [loadingAI, setLoadingAI] = useState(false);
  const [loadingCoach, setLoadingCoach] = useState(false);
  const [currentPage, setCurrentPage] = useState("dashboard");

  const generateAIReport = async () => {

    setLoadingCoach(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/ai-coach"
      );

      const data = await response.json();

      setCoach(data);

    } catch {

      alert("AI service unavailable");

    }

    setLoadingCoach(false);

  };

  const askAI = async () => {

    if (!question.trim()) return;

    setLoadingAI(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/ask-ai",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            question
          })
        }
      );

      const data = await response.json();

      setAiResponse(data.response);

    } catch (error) {

      setAiResponse(
        "Unable to contact AI Assistant."
      );

    }

    setLoadingAI(false);
  };

  const chartData = [
    {
      name: "Coding",
      value: insights.coding || 0,
    },
    {
      name: "Browsing",
      value: insights.browsing || 0,
    },
    {
      name: "Email",
      value: insights.email || 0,
    },
  ];

  const COLORS = ["#6C63FF", "#00C9A7", "#FFB84C"];

  useEffect(() => {
    const fetchData = () => {
      fetch("http://127.0.0.1:8000/activities")
        .then((res) => res.json())
        .then((data) => setActivities(data));

      fetch("http://127.0.0.1:8000/suggestions")
        .then((res) => res.json())
        .then((data) => setSuggestions(data));

      fetch("http://127.0.0.1:8000/productivity-score")
        .then((res) => res.json())
        .then((data) => setScore(data));

      fetch("http://127.0.0.1:8000/ai-insights")
      .then(res => res.json())
      .then(data => {

          setInsights(data.behavior.counts);

          setAiInsights(
              data.behavior.insights
          );

          setFocus(
              data.focus
          );

      });

      fetch("http://127.0.0.1:8000/daily-summary")
        .then(res => res.json())
        .then(data => setDailySummary(data.summary));

      fetch("http://127.0.0.1:8000/categorized-activities")
      .then(res=>res.json())
      .then(data=>setCategorized(data))    

     /* fetch("http://127.0.0.1:8000/ai-coach")
      .then(res => res.json())
      .then(data => setCoach(data));*/

      fetch("http://127.0.0.1:8000/current-app")
      .then(res => res.json())
      .then(data => setCurrentApp(data));

      fetch("http://127.0.0.1:8000/live-status")
      .then(res => res.json())
      .then(data => setLiveStatus(data));
      
      fetch("http://127.0.0.1:8000/hourly-activity")
      .then(res => res.json())
      .then(data => {

        const formatted =
          Object.entries(data).map(([hour,count])=>({

            hour: `${hour}:00`,
            value: count

          }));

        setTimelineData(formatted);

      });
        
    };


    fetchData();

    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  const topApps = categorized
    .reduce((acc, item) => {
      acc[item.app] = (acc[item.app] || 0) + 1;
      return acc;
    }, {});  

  {currentPage === "dashboard" && (
    <>
      ALL CURRENT DASHBOARD CODE
    </>
  )}

  {currentPage === "analytics" && (

  <div className="page-card">

    <h1>📊 Analytics</h1>

    <div className="stats-grid">

      <div className="stat-card">
        <h2>{activities.length}</h2>
        <p>Total Activities</p>
      </div>

      <div className="stat-card">
        <h2>{score.score}</h2>
        <p>Productivity Score</p>
      </div>

      <div className="stat-card">
        <h2>{insights.browsing}</h2>
        <p>Browsing</p>
      </div>

      <div className="stat-card">
        <h2>{insights.email}</h2>
        <p>Email</p>
      </div>

    </div>

    <div className="activities-card">

      <h2>Top Applications</h2>

      {activities.slice(0,10).map((item,index)=>(

        <div
          key={index}
          className="activity-item"
        >
          <h4>{item.category}</h4>
          <span>{item.app}</span>
        </div>

      ))}

    </div>

  </div>

  )}
  {currentPage === "focus" && (

  <div className="page-card">

    <h1>🎯 Focus Mode</h1>

    <div className="focus-card">

      <h3>Current App</h3>

      <p>{currentApp.app}</p>

      <h3>Category</h3>

      <p>{liveStatus.category}</p>

      <h3>Status</h3>

      <p>{focus.message}</p>

      <button className="ai-button">
        Start Focus Session
      </button>

      <button 
        className="ai-button">
        style={{marginLeft:"10px"}}
        Stop Focus Session
      </button>
    </div>
  </div>

  )}

  {currentPage === "insights" && (

  <div className="page-card">

  <h2>🧠 Insights</h2>

  {
  aiInsights.map((item,index)=>(

  <p key={index}>
  ✓ {item}
  </p>

  ))
  }

  </div>

  )}
  {currentPage === "settings" && (

  <div className="page-card">

    <h1>⚙️ Settings</h1>

    <div className="activities-card">

      <div className="activity-item">
        <h4>Tracker</h4>
        <span>🟢 Running</span>
      </div>

      <div className="activity-item">
        <h4>Backend</h4>
        <span>🟢 Online</span>
      </div>

      <div className="activity-item">
        <h4>Database</h4>
        <span>🟢 Connected</span>
      </div>

      <div className="activity-item">
        <h4>n8n</h4>
        <span>🟢 Installed</span>
      </div>

      <div className="activity-item">
        <h4>AI Assistant</h4>
        <span>⚪ Disabled</span>
      </div>

    </div>

  </div>

  )}
  return (
    <div className="app-container">
      <aside className="sidebar">
        <div>
          <h1 className="logo">AI Work</h1>
          <p className="sub-logo">Your Personalised Assistant</p>
        </div>

        <div className="nav-links">

          <button
            className={currentPage === "dashboard" ? "active-nav" : ""}
            onClick={() => setCurrentPage("dashboard")}
          >
            Dashboard
          </button>

          <button
            className={currentPage === "analytics" ? "active-nav" : ""}
            onClick={() => setCurrentPage("analytics")}
          >
            Analytics
          </button>

          <button
            className={currentPage === "focus" ? "active-nav" : ""}
            onClick={() => setCurrentPage("focus")}
          >
            Focus Mode
          </button>

          <button
            className={currentPage === "insights" ? "active-nav" : ""}
            onClick={() => setCurrentPage("insights")}
          >
            Insights
          </button>
          <button
            className={currentPage === "reports" ? "active-nav" : ""}
            onClick={() => setCurrentPage("reports")}
          >
            Reports
          </button>

          <button
            className={currentPage === "settings" ? "active-nav" : ""}
            onClick={() => setCurrentPage("settings")}
          >
            Settings
          </button>

        </div>


        <div className="sidebar-footer">
          <p>Realtime Productivity Tracker</p>
        </div>
      </aside>

      <main className="main-content">
      {currentPage === "dashboard" && (
      <>
        <div className="top-bar">
          <div>
            <h1>Productivity Dashboard</h1>
            <p>Monitor your work habits in realtime</p>
          </div>

          <div className="live-badge">
            <span className="dot"></span>
            Live Tracking
          </div>
        </div>

        <section className="current-section">

          <div className="current-card">

            <h3>⚡ Current Activity</h3>

            <h2>
              {currentApp.app || "Unknown App"}
            </h2>

            <p>
              {currentApp.title || "No active window"}
            </p>

            <span className="activity-status">
              {liveStatus.category || "Unknown"}
            </span>

          </div>

        </section>
        <section className="summary-banner">

          <div className="summary-banner-card">

            <h2>📋 Daily Executive Summary</h2>

            <p>
              {dailySummary}
            </p>

          </div>

        </section>
        
        <section className="score-section">
          <div className="score-card">
            <h3>Productivity Score</h3>
            <div className="score-circle">
              <h1>{score.score || 0}</h1>
              <span>/100</span>
            </div>

            <div className="alerts">
              {score.alerts?.map((item, index) => (
                <p key={index}>⚠️ {item}</p>
              ))}
            </div>
          </div>

          <div className="timeline-card">
            <div className="card-header">
              <h3>Activity Timeline</h3>
              <p>Most active hours today</p>
            </div>

            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={timelineData}>
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke="#6C63FF"
                  fill="#6C63FF"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="stats-grid">
          <div className="stat-card coding-card">
            <h2>{insights.coding || 0}</h2>
            <p>Coding Sessions</p>
          </div>

          <div className="stat-card browsing-card">
            <h2>{insights.browsing || 0}</h2>
            <p>Browsing Sessions</p>
          </div>

          <div className="stat-card email-card">
            <h2>{insights.email || 0}</h2>
            <p>Email Sessions</p>
          </div>
        </section>

        <section className="middle-grid">

          <div className="chart-card">

            <div className="card-header">
              <h3>Work Distribution</h3>
              <p>Realtime usage analysis</p>
            </div>

            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={70}                  
                  label
                >
                  {chartData.map((entry, index) => (
                    <Cell
                      key={index}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>

                <Tooltip />
              </PieChart>
            </ResponsiveContainer>

          </div>

          <div>

            <div className="focus-card">

              <div className="card-header">
                <h3>🎯 Focus Monitor</h3>
              </div>

              <div className="summary-item">

                <h4>Status</h4>

                <p>{focus.message}</p>

                <h4>Current App</h4>

                <p>{currentApp.app}</p>

                <h4>Category</h4>

                <p>{liveStatus.category}</p>

              </div>

            </div>

          </div>
          

        </section>

        <section className="bottom-grid">
          <div className="activities-card">
            <div className="card-header">
              <h3>Recent Activities</h3>
              <p>Realtime application tracking</p>
            </div>

            <div className="activities-list">

              {categorized.map((item,index)=>(

              <div
              key={index}
              className="activity-item"
              >

              <div>

              <h4>{item.category}</h4>

              <p>{item.app}</p>

              </div>

              <div>

              <span className="activity-status">
              {new Date(item.time).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit"
              })}
              </span>

              </div>

              </div>

              ))}

              </div>
          </div>

        </section>
        </>
        )}
        {currentPage === "analytics" && (

        <div className="page-card">

        <h1>📊 Analytics</h1>

        <h3>Category Breakdown</h3>

        <p>Coding: {insights.coding || 0}</p>
        <p>Browsing: {insights.browsing || 0}</p>
        <p>Email: {insights.email || 0}</p>

        </div>

        )}
        {currentPage === "insights" && (

        <div className="page-card">

        <h1>🧠 Insights</h1>

        {
        aiInsights.map((item,index)=>(
        <p key={index}>✓ {item}</p>
        ))
        }

        </div>

        )}
        {currentPage === "focus" && (

        <div className="page-card">

        <h1>🎯 Focus Mode</h1>

        <p>Current App: {currentApp.app}</p>

        <p>Category: {liveStatus.category}</p>

        <p>{focus.message}</p>

        </div>

        )}

        {currentPage === "settings" && (

        <div className="page-card">

        <h1>⚙️ Settings</h1>

        <p>Database: Connected</p>

        <p>Tracker: Running</p>

        <p>Backend: Online</p>

        <p>n8n: Connected</p>

        </div>

        )}
        {currentPage === "reports" && (

        <div className="page-card">

          <h1>📄 Reports</h1>

          <div className="activity-item">
            <h4>Productivity Score</h4>
            <span>{score?.score || 0}/100</span>
          </div>

          <div className="activity-item">
            <h4>Status</h4>
            <span>Ready for Export</span>
          </div>

        </div>

        )}

      </main>
    </div>
  );
}

export default App;