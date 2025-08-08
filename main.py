// This is a React application for a Nexus build board.
// It is designed to be lightweight and stable, focusing on displaying the status
// of different simulated bot processes or 'builds'.

import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom/client';

// Tailwind CSS is assumed to be available
const App = () => {
  return (
    <div className="bg-[#080d12] text-[#00ffc0] font-mono min-h-screen flex items-center justify-center overflow-hidden">
      <div className="container relative w-[95vw] h-[95vh] bg-black/70 border-2 border-[#00ffc0] shadow-[0_0_20px_#00ffc0] grid grid-cols-1 p-4 gap-4 z-10 rounded-2xl">
        <header className="border-b-2 border-[#00ffc0] pb-2 flex justify-between items-center">
          <div className="text-3xl font-bold font-orbitron">
            NEXUS // BUILD_BOARD
          </div>
          <div className="text-sm">
            STATUS: ACTIVE
          </div>
        </header>
        <main className="h-full overflow-hidden">
          <MainBuildBoard />
        </main>
      </div>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
        
        .font-orbitron { font-family: 'Orbitron', sans-serif; }
        .font-mono { font-family: 'Share Tech Mono', monospace; }
        
        .status-success { color: #00ffc0; }
        .status-failed { color: #ff0055; }
        .status-progress { color: #ffc000; }
      `}</style>
    </div>
  );
};

// Main Build Board view with job status and a log
const MainBuildBoard = () => {
  const [jobs, setJobs] = useState([
    { id: 1, name: 'Nexus-Core-Update', status: 'Success', timestamp: '2025-08-08 10:01:23' },
    { id: 2, name: 'Network-Monitor-v1.2', status: 'Success', timestamp: '2025-08-08 09:55:10' },
    { id: 3, name: 'API-Integration-Module', status: 'Failed', timestamp: '2025-08-08 09:42:05' },
    { id: 4, name: 'Security-Patch-Deployment', status: 'Success', timestamp: '2025-08-08 09:30:45' },
    { id: 5, name: 'UI-Dashboard-Build', status: 'Success', timestamp: '2025-08-08 09:20:11' },
    { id: 6, name: 'Log-Parsing-Script', status: 'Success', timestamp: '2025-08-08 09:15:30' },
    { id: 7, name: 'New-Module-Test', status: 'In Progress', timestamp: '2025-08-08 10:05:00' },
  ]);

  // Simulate a new job every 10 seconds
  useEffect(() => {
    const jobNames = ['Database-Sync', 'Core-Module-Compile', 'Data-Validation-Check', 'Service-Restart'];
    const interval = setInterval(() => {
      const newJob = {
        id: jobs.length + 1,
        name: jobNames[Math.floor(Math.random() * jobNames.length)],
        status: 'In Progress',
        timestamp: new Date().toISOString().substring(0, 19).replace('T', ' '),
      };
      setJobs(prevJobs => {
        // Find if any job is currently in progress and set it to a final status
        const updatedJobs = prevJobs.map(job => {
          if (job.status === 'In Progress') {
            const newStatus = Math.random() > 0.3 ? 'Success' : 'Failed';
            return { ...job, status: newStatus };
          }
          return job;
        });
        return [newJob, ...updatedJobs].slice(0, 7); // Keep only the last 7 jobs
      });
    }, 10000);

    return () => clearInterval(interval);
  }, [jobs.length]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 h-full">
      <div className="data-panel flex flex-col p-4 bg-black/50 border border-[#00ffc0] rounded-lg">
        <h2 className="text-xl mb-4 text-[#00ffc0]">RECENT_BUILDS</h2>
        <div className="flex flex-col gap-2 overflow-y-auto">
          {jobs.map(job => (
            <BuildJob key={job.id} job={job} />
          ))}
        </div>
      </div>
      <div className="data-panel flex flex-col p-4 bg-black/50 border border-[#00ffc0] rounded-lg">
        <h2 className="text-xl mb-4 text-[#00ffc0]">SYSTEM_LOGS</h2>
        <SystemLog />
      </div>
    </div>
  );
};

// Component for a single build job entry
const BuildJob = ({ job }) => {
  let statusColorClass = 'status-progress';
  let statusEmoji = '⚙️';
  if (job.status === 'Success') {
    statusColorClass = 'status-success';
    statusEmoji = '✅';
  } else if (job.status === 'Failed') {
    statusColorClass = 'status-failed';
    statusEmoji = '❌';
  }

  return (
    <div className={`p-2 border border-[#00ffc0] rounded-lg flex justify-between items-center ${statusColorClass}`}>
      <div className="flex items-center gap-2">
        <span className="text-xl">{statusEmoji}</span>
        <div>
          <p className="font-orbitron text-lg">{job.name}</p>
          <p className="text-xs text-gray-400">{job.timestamp}</p>
        </div>
      </div>
      <p className="font-bold">{job.status.toUpperCase()}</p>
    </div>
  );
};

// Component for a simulated log stream
const SystemLog = () => {
  const [logs, setLogs] = useState([]);
  const logRef = useRef(null);

  useEffect(() => {
    const logInterval = setInterval(() => {
      const logMessages = [
        'INFO: Starting new build process for Network-Monitor',
        'SUCCESS: Build Network-Monitor completed in 12.5s',
        'INFO: Triggering Nexus-Core-Update',
        'ERROR: Failed to connect to API endpoint during build',
        'INFO: Reverting to previous stable build',
        'SUCCESS: Rollback complete. System stable.',
        'WARNING: High CPU load detected on build server',
        'INFO: Build queue is empty. Awaiting new tasks.'
      ];
      const randomLog = logMessages[Math.floor(Math.random() * logMessages.length)];
      setLogs(prevLogs => [...prevLogs, `[${new Date().toISOString().substring(11, 19)}] ${randomLog}`].slice(-100)); // Keep only the last 100 logs
    }, 1000);

    return () => clearInterval(logInterval);
  }, []);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="flex flex-col h-full overflow-y-auto whitespace-pre-wrap break-words p-2 bg-black/50 border border-[#00ffc0] rounded-lg">
      <div ref={logRef}>
        {logs.map((line, index) => <div key={index}>{line}</div>)}
      </div>
    </div>
  );
};

export default App;
