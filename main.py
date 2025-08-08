// This is a self-contained React application for a futuristic dashboard.
// It is designed to run entirely in the browser, eliminating server-side errors.
// All bot data is simulated and updated with client-side state.

import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom/client';
import * as THREE from 'three';

// Tailwind CSS is assumed to be available
const App = () => {
  const [isBooted, setIsBooted] = useState(false);
  const handleBootComplete = () => setIsBooted(true);

  // Main App Component
  return (
    <div className="bg-[#080d12] text-[#00ffc0] font-mono min-h-screen flex items-center justify-center overflow-hidden [perspective:1000px]">
      <div className="container relative w-[95vw] h-[95vh] bg-black/70 border-2 border-[#00ffc0] shadow-[0_0_20px_#00ffc0] animate-border-pulse grid grid-cols-1 md:grid-cols-[1fr_2fr_1fr] md:grid-rows-[auto_1fr_1fr] p-4 gap-4 z-10 rounded-2xl">
        <header className="header md:col-span-3 border-b-2 border-[#00ffc0] pb-2 flex justify-between items-center">
          <div className="text-3xl font-bold font-orbitron glitch-text">
            NEXUS // SYSTEM_STATUS
          </div>
          <div className="text-sm">
            {isBooted ? 'ONLINE // OPERATIONAL' : 'BOOTING...'}
          </div>
        </header>
        <main className="md:col-span-3 h-full overflow-hidden">
          {isBooted ? <MainDashboard /> : <TerminalSimulator onBootComplete={handleBootComplete} />}
        </main>
      </div>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
        
        .font-orbitron { font-family: 'Orbitron', sans-serif; }
        .font-mono { font-family: 'Share Tech Mono', monospace; }

        @keyframes border-pulse {
          0% { box-shadow: 0 0 10px #00ffc0; }
          50% { box-shadow: 0 0 30px #00ffc0, 0 0 5px #00ffc0 inset; }
          100% { box-shadow: 0 0 10px #00ffc0; }
        }
        @keyframes glitch {
          0%   { transform: translate(0); }
          20%  { transform: translate(-2px, 2px); }
          40%  { transform: translate(-2px, -2px); }
          60%  { transform: translate(2px, 2px); }
          80%  { transform: translate(2px, -2px); }
          100% { transform: translate(0); }
        }
        @keyframes text-pulse {
            0% { color: #00ffc0; }
            50% { color: #80ffe0; }
            100% { color: #00ffc0; }
        }
      `}</style>
    </div>
  );
};

// Main Dashboard view with all the panels
const MainDashboard = () => {
  // We will manage all our state here and pass it down
  const [status, setStatus] = useState({
    uptime_seconds: 0,
    ping_ms: 'N/A',
    load: 0,
  });

  // Use a single useEffect to handle all simulated data updates
  useEffect(() => {
    // Simulate ping, load, and uptime updates
    const interval = setInterval(() => {
      setStatus(prevStatus => ({
        uptime_seconds: prevStatus.uptime_seconds + 1,
        ping_ms: Math.round(Math.random() * 50) + 20, // Simulate ping between 20-70ms
        load: Math.round(Math.random() * 60) + 20,   // Simulate load between 20-80%
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const formatUptime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    return `${hours}h ${minutes}m ${remainingSeconds}s`;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr_1fr] md:grid-rows-[1fr_1fr] gap-4 h-full">
      <div className="data-panel md:col-span-1 md:row-span-2">
        <h2 className="text-xl mb-2 text-[#00ffc0]">NETWORK_VISUALIZER</h2>
        <ParticleSystem systemLoad={status.load} />
      </div>
      <div className="data-panel md:col-span-2 md:row-span-1">
        <h2 className="text-xl mb-2 text-[#00ffc0]">DATA_STREAM</h2>
        <DataWaveform />
      </div>
      <div className="data-panel md:col-span-2 md:row-span-1">
        <h2 className="text-xl mb-2 text-[#00ffc0]">SYSTEM_CONTROL</h2>
        <SystemControlTerminal />
      </div>
      <div className="data-panel md:col-span-1 md:row-span-1 flex flex-col justify-center">
        <StatusPanel title="SYSTEM_UPTIME" value={formatUptime(status.uptime_seconds)} />
        <div className="h-px bg-[#00ffc0] my-4" />
        <StatusPanel title="SYSTEM_PING" value={status.ping_ms === 'N/A' ? status.ping_ms : status.ping_ms + "ms"} />
      </div>
      <div className="data-panel md:col-span-1 md:row-span-1">
        <NexusInfoPanel info="This is a highly-advanced, self-monitoring AI construct designed to manage, secure, and interact with network environments. It is a fusion of a multi-modal perception core and an adaptive logic engine. Its primary directive is to maintain system integrity and provide advanced utility functions to its administrators." />
        <div className="h-px bg-[#00ffc0] my-4" />
        <InviteNexusPanel inviteUrl="#" /> {/* Placeholder for the bot invite URL */}
      </div>
    </div>
  );
};

// Component for the simulated boot sequence
const TerminalSimulator = ({ onBootComplete }) => {
  const [logs, setLogs] = useState([]);
  const logRef = useRef(null);

  useEffect(() => {
    const bootSequence = [
      'INITIALIZING SYSTEM PROTOCOLS...',
      'LOADING NEXUS-CORE v7.1.2...',
      'AUTH: CHECKING API CREDENTIALS...',
      'AUTH: DISCORD_BOT_SECRET [OK]',
      'NETWORK: ATTEMPTING CONNECTION...',
      'NETWORK: CONNECTION ESTABLISHED. PING: 34ms',
      'NETWORK: DATA CHANNELS SYNCHRONIZED.',
      'DATABASE: CONNECTING TO COMMAND_LOGS...',
      'DATABASE: CONNECTION SECURE. ACCESS GRANTED.',
      'SYSTEM: ALL MODULES REPORTING OPERATIONAL.',
      'SECURITY: FIREWALLS ONLINE.',
      'SECURITY: INTRUSION_DETECTION [ACTIVE]',
      'SYSTEM BOOT COMPLETE. ENTERING MAIN OPERATIONAL MODE.',
    ];
    
    let logIndex = 0;
    const interval = setInterval(() => {
      if (logIndex < bootSequence.length) {
        setLogs(prev => [...prev, `[${new Date().toISOString()}] >> ${bootSequence[logIndex]}`]);
        logIndex++;
      } else {
        clearInterval(interval);
        setTimeout(onBootComplete, 1500);
      }
    }, 300);
    
    return () => clearInterval(interval);
  }, [onBootComplete]);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="p-4 bg-[#00ffc0]/5 border border-[#00ffc0] rounded-lg h-full flex flex-col">
      <h2 className="font-orbitron text-2xl mb-2 text-[#00ffc0]">SYSTEM_BOOT_SEQUENCE</h2>
      <div ref={logRef} className="flex-grow overflow-y-auto whitespace-pre-wrap break-words text-sm">
        {logs.map((log, index) => <div key={index}>{log}</div>)}
      </div>
    </div>
  );
};

// Component for the particle system visualization using Three.js
const ParticleSystem = ({ systemLoad }) => {
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const particlesRef = useRef([]);
  const linesRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    sceneRef.current = new THREE.Scene();
    cameraRef.current = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    rendererRef.current = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    rendererRef.current.setSize(width, height);
    containerRef.current.appendChild(rendererRef.current.domElement);

    cameraRef.current.position.z = 20;

    const particleCount = 500;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i++) {
      positions[i] = (Math.random() - 0.5) * 100;
    }
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const material = new THREE.PointsMaterial({
      color: 0x00ffc0,
      size: 0.5,
      transparent: true,
      opacity: 0.8
    });
    const particleMesh = new THREE.Points(geometry, material);
    sceneRef.current.add(particleMesh);
    particlesRef.current = Array.from({ length: particleCount }, (_, i) => new THREE.Vector3(positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]));

    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x00ffc0,
      transparent: true,
      opacity: 0.1
    });
    const lineGeometry = new THREE.BufferGeometry();
    const linePositions = new Float32Array(particleCount * particleCount * 3);
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    linesRef.current = new THREE.LineSegments(lineGeometry, lineMaterial);
    sceneRef.current.add(linesRef.current);

    const animate = () => {
      requestAnimationFrame(animate);

      const linePositionsArray = linesRef.current.geometry.attributes.position.array;
      let lineIndex = 0;

      for (let i = 0; i < particleCount; i++) {
        for (let j = i + 1; j < particleCount; j++) {
          const p1 = particlesRef.current[i];
          const p2 = particlesRef.current[j];
          const distance = p1.distanceTo(p2);
          const maxDistance = 20 + (systemLoad / 10);
          if (distance < maxDistance) {
            linePositionsArray[lineIndex++] = p1.x;
            linePositionsArray[lineIndex++] = p1.y;
            linePositionsArray[lineIndex++] = p1.z;

            linePositionsArray[lineIndex++] = p2.x;
            linePositionsArray[lineIndex++] = p2.y;
            linePositionsArray[lineIndex++] = p2.z;
          }
        }
      }

      for (let i = lineIndex; i < linePositionsArray.length; i++) {
        linePositionsArray[i] = 0;
      }
      linesRef.current.geometry.attributes.position.needsUpdate = true;
      linesRef.current.geometry.setDrawRange(0, lineIndex);

      particlesRef.current.forEach(p => {
        const speed = systemLoad / 10000;
        p.x += (Math.random() - 0.5) * speed;
        p.y += (Math.random() - 0.5) * speed;
        p.z += (Math.random() - 0.5) * speed;
      });
      particleMesh.geometry.attributes.position.needsUpdate = true;
      
      rendererRef.current.render(sceneRef.current, cameraRef.current);
    };

    const handleResize = () => {
      if (containerRef.current) {
        const newWidth = containerRef.current.clientWidth;
        const newHeight = containerRef.current.clientHeight;
        rendererRef.current.setSize(newWidth, newHeight);
        cameraRef.current.aspect = newWidth / newHeight;
        cameraRef.current.updateProjectionMatrix();
      }
    };
    
    animate();
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      if (containerRef.current && rendererRef.current.domElement) {
        containerRef.current.removeChild(rendererRef.current.domElement);
      }
      rendererRef.current.dispose();
    };
  }, [systemLoad]);

  return (
    <div ref={containerRef} className="w-full h-full min-h-[300px]" />
  );
};

// Component for the data waveform visualization on a canvas
const DataWaveform = () => {
  const canvasRef = useRef(null);
  const dataHistory = useRef([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    const draw = () => {
      const parent = canvas.parentElement;
      const width = parent.clientWidth;
      const height = parent.clientHeight;
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
      }

      ctx.clearRect(0, 0, width, height);

      const now = new Date();
      const seconds = now.getSeconds();
      const milliseconds = now.getMilliseconds();
      const isGlitch = seconds % 10 === 0 && milliseconds < 100;
      const glitchColor = isGlitch ? '#ff0055' : '#00ffc0';

      ctx.strokeStyle = glitchColor;
      ctx.lineWidth = 2;
      ctx.beginPath();
      
      const newData = Math.sin(Date.now() / 500) * 0.5 + Math.cos(Date.now() / 700) * 0.3 + 0.5;
      dataHistory.current.push(newData);
      if (dataHistory.current.length > width / 5) {
        dataHistory.current.shift();
      }

      dataHistory.current.forEach((value, index) => {
        const x = index * 5;
        const y = height - (value * height);
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();

      if (isGlitch) {
        ctx.strokeStyle = '#ff0055';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(Math.random() * width, 0);
        ctx.lineTo(Math.random() * width, height);
        ctx.stroke();
      }

      animationFrameId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return <canvas ref={canvasRef} className="glowing-canvas w-full h-full min-h-[150px]" />;
};

// Component for the simulated command terminal
const SystemControlTerminal = () => {
  const [history, setHistory] = useState([
    'Nexus Command-Line Interface v7.1.2',
    'Type "help" for a list of commands.',
    '>>'
  ]);
  const [input, setInput] = useState('');
  const terminalRef = useRef(null);

  const handleCommand = (e) => {
    if (e.key === 'Enter' && input.trim() !== '') {
      const command = input.trim();
      const newHistory = [...history, `>> ${command}`];
      const [cmd, ...args] = command.split(' ');

      let response = '';
      switch(cmd) {
        case 'help':
          response = 'Available commands:\n- status: Display current system status.\n- connect [ID]: Attempt to connect to a specific module.\n- echo [message]: Repeat the given message.\n- clear: Clear the terminal output.';
          break;
        case 'status':
          response = 'STATUS: SIMULATED (ONLINE)\nUPTIME: Client-side simulation\nMODULES: 7/7 ACTIVE\nLOAD: Simulated';
          break;
        case 'connect':
          if (args.length > 0) {
            response = `CONNECTING TO MODULE ${args[0]}... \n[SUCCESS] CONNECTION SECURE.`;
          } else {
            response = 'ERROR: No module ID provided.';
          }
          break;
        case 'echo':
          if (args.length > 0) {
            response = args.join(' ');
          } else {
            response = 'ERROR: No message to echo.';
          }
          break;
        case 'clear':
          setHistory(['Nexus Command-Line Interface v7.1.2', 'Type "help" for a list of commands.', '>>']);
          setInput('');
          return;
        default:
          response = `ERROR: Command "${cmd}" not found.`;
          break;
      }
      setHistory([...newHistory, response, '>>']);
      setInput('');
    }
  };

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [history]);

  return (
    <div className="flex flex-col h-full">
      <div className="flex-grow overflow-y-auto whitespace-pre-wrap break-words p-2" ref={terminalRef}>
        {history.map((line, index) => <div key={index}>{line}</div>)}
      </div>
      <input
        type="text"
        className="terminal-input bg-[#00ffc0]/10 border border-[#00ffc0] p-2 text-[#00ffc0] rounded-md outline-none w-full box-border mt-auto"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleCommand}
        autoFocus
      />
    </div>
  );
};

// Simple status panel component
const StatusPanel = ({ title, value }) => (
  <div className="flex-1 flex flex-col justify-center">
    <h2 className="text-xl mb-2 text-[#00ffc0]">{title}</h2>
    <p className="text-2xl text-center font-orbitron">{value}</p>
  </div>
);

// Bot information panel
const NexusInfoPanel = ({ info }) => (
  <div className="flex flex-col h-full justify-center">
    <h2 className="text-xl mb-2 text-[#00ffc0]">NEXUS_INFO</h2>
    <p className="text-sm text-center">{info}</p>
  </div>
);

// Bot invite button panel
const InviteNexusPanel = ({ inviteUrl }) => (
  <div className="flex flex-col h-full justify-center">
    <h2 className="text-xl mb-2 text-[#00ffc0]">INVITE_NEXUS</h2>
    <a href={inviteUrl} target="_blank" rel="noopener noreferrer" className="bg-[#00ffc0] text-[#080d12] p-4 text-2xl font-bold rounded-lg text-center cursor-pointer shadow-[0_0_10px_#00ffc0] animate-[button-pulse_1.5s_infinite_ease-in-out] mt-4 hover:bg-[#80ffe0] hover:shadow-[0_0_20px_#80ffe0]">
      INVITE NEXUS
    </a>
  </div>
);

export default App;
