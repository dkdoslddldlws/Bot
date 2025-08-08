# main.py
# This code sets up a Discord bot and a Flask web server with a dynamic,
# 3D-enabled and D3.js-powered dashboard built with React.
# This version includes a dedicated bot info panel, an invite button,
# a command usage chart, and an interactive message sending feature.

import os
import threading
import discord
from discord.ext import commands
from flask import Flask, request, render_template_string, jsonify
import random
import time
import hashlib
from collections import defaultdict
import datetime

# ====================
# React Dashboard as a String
# ====================

# This is the entire React application code, which will be served by Flask.
# It uses React with hooks, Three.js for a custom particle visualization,
# a hand-coded canvas for data streaming, and a simulated terminal.
react_dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBER-BOT // SYSTEM_STATUS</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');
        body {
            font-family: 'Share Tech Mono', monospace;
            background-color: #080d12;
            color: #00ffc0;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            perspective: 1000px;
        }
        .container {
            width: 95vw;
            height: 95vh;
            background-color: rgba(0, 0, 0, 0.7);
            border: 2px solid #00ffc0;
            box-shadow: 0 0 20px #00ffc0;
            position: relative;
            animation: border-pulse 4s infinite ease-in-out;
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            grid-template-rows: auto 1fr 1fr;
            padding: 1rem;
            gap: 1rem;
            z-index: 10;
        }
        @keyframes border-pulse {
            0% { box-shadow: 0 0 10px #00ffc0; }
            50% { box-shadow: 0 0 30px #00ffc0, 0 0 5px #00ffc0 inset; }
            100% { box-shadow: 0 0 10px #00ffc0; }
        }
        .header {
            font-family: 'Orbitron', sans-serif;
            border-bottom: 1px solid #00ffc0;
            padding-bottom: 0.5rem;
            grid-column: 1 / -1;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .glitch-text {
            animation: glitch 1.5s infinite;
        }
        @keyframes glitch {
            0%   { transform: translate(0); }
            20%  { transform: translate(-2px, 2px); }
            40%  { transform: translate(-2px, -2px); }
            60%  { transform: translate(2px, 2px); }
            80%  { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
        .data-panel {
            background-color: rgba(0, 255, 192, 0.05);
            border: 1px solid rgba(0, 255, 192, 0.2);
            padding: 1rem;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
            backdrop-filter: blur(2px);
            border-radius: 8px;
        }
        .data-panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 255, 192, 0.05),
                rgba(0, 255, 192, 0.05) 1px,
                transparent 1px,
                transparent 10px
            );
            z-index: 0;
        }
        .scrollable-content {
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: #00ffc0 #080d12;
            padding-right: 0.5rem;
        }
        .scrollable-content::-webkit-scrollbar {
            width: 8px;
        }
        .scrollable-content::-webkit-scrollbar-track {
            background: #080d12;
        }
        .scrollable-content::-webkit-scrollbar-thumb {
            background-color: #00ffc0;
            border-radius: 4px;
        }
        .pulse-text {
            animation: text-pulse 2s infinite ease-in-out;
        }
        @keyframes text-pulse {
            0% { color: #00ffc0; }
            50% { color: #80ffe0; }
            100% { color: #00ffc0; }
        }
        #canvas-container {
            width: 100%;
            height: 100%;
            min-height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .invite-button {
            background-color: #00ffc0;
            color: #080d12;
            padding: 1rem 2rem;
            font-size: 1.25rem;
            font-weight: bold;
            border-radius: 0.5rem;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 0 10px #00ffc0;
            animation: button-pulse 1.5s infinite ease-in-out;
        }
        .invite-button:hover {
            background-color: #80ffe0;
            box-shadow: 0 0 20px #80ffe0;
        }
        @keyframes button-pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .terminal-input {
            background-color: rgba(0, 255, 192, 0.1);
            border: 1px solid #00ffc0;
            padding: 8px;
            color: #00ffc0;
            border-radius: 4px;
            font-family: 'Share Tech Mono', monospace;
            outline: none;
            width: 100%;
            box-sizing: border-box;
        }
        .terminal-output {
            flex-grow: 1;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            padding: 0.5rem;
        }
        .glowing-canvas {
            filter: drop-shadow(0 0 8px #00ffc0);
        }
    </style>
</head>
<body>
    <div id="root"></div>
    <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    
    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        function ParticleSystem({ systemLoad }) {
            const containerRef = useRef(null);
            const scene = useRef(null);
            const camera = useRef(null);
            const renderer = useRef(null);
            const particles = useRef([]);
            const lines = useRef(null);

            useEffect(() => {
                if (!containerRef.current) return;

                const width = containerRef.current.clientWidth;
                const height = containerRef.current.clientHeight;

                scene.current = new THREE.Scene();
                camera.current = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
                renderer.current = new THREE.WebGLRenderer({ antialias: true, alpha: true });
                renderer.current.setSize(width, height);
                containerRef.current.appendChild(renderer.current.domElement);

                camera.current.position.z = 20;

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
                scene.current.add(particleMesh);
                particles.current = Array.from({ length: particleCount }, (_, i) => new THREE.Vector3(positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2]));

                const lineMaterial = new THREE.LineBasicMaterial({
                    color: 0x00ffc0,
                    transparent: true,
                    opacity: 0.1
                });
                const lineGeometry = new THREE.BufferGeometry();
                const linePositions = new Float32Array(particleCount * particleCount * 3);
                lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
                lines.current = new THREE.LineSegments(lineGeometry, lineMaterial);
                scene.current.add(lines.current);

                const animate = () => {
                    requestAnimationFrame(animate);

                    const linePositionsArray = lines.current.geometry.attributes.position.array;
                    let lineIndex = 0;

                    for (let i = 0; i < particleCount; i++) {
                        for (let j = i + 1; j < particleCount; j++) {
                            const p1 = particles.current[i];
                            const p2 = particles.current[j];
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
                    lines.current.geometry.attributes.position.needsUpdate = true;
                    lines.current.geometry.setDrawRange(0, lineIndex);

                    particles.current.forEach(p => {
                        const speed = systemLoad / 1000;
                        p.x += (Math.random() - 0.5) * speed;
                        p.y += (Math.random() - 0.5) * speed;
                        p.z += (Math.random() - 0.5) * speed;
                    });
                    particleMesh.geometry.attributes.position.needsUpdate = true;
                    
                    renderer.current.render(scene.current, camera.current);
                };

                const handleResize = () => {
                    const newWidth = containerRef.current.clientWidth;
                    const newHeight = containerRef.current.clientHeight;
                    renderer.current.setSize(newWidth, newHeight);
                    camera.current.aspect = newWidth / newHeight;
                    camera.current.updateProjectionMatrix();
                };
                
                animate();
                window.addEventListener('resize', handleResize);
                return () => {
                    window.removeEventListener('resize', handleResize);
                    containerRef.current.removeChild(renderer.current.domElement);
                    renderer.current.dispose();
                };
            }, [systemLoad]);

            return <div ref={containerRef} style={{ width: '100%', height: '100%', minHeight: '300px' }}></div>;
        }

        function DataWaveform() {
            const canvasRef = useRef(null);
            const dataHistory = useRef([]);

            useEffect(() => {
                const canvas = canvasRef.current;
                const ctx = canvas.getContext('2d');
                let animationFrameId;

                const draw = () => {
                    const width = canvas.width;
                    const height = canvas.height;
                    ctx.clearRect(0, 0, width, height);

                    const now = new Date();
                    const seconds = now.getSeconds();
                    const milliseconds = now.getMilliseconds();
                    const isGlitch = seconds % 10 === 0 && milliseconds < 100;
                    const glitchColor = isGlitch ? '#ff0055' : '#00ffc0';

                    ctx.strokeStyle = glitchColor;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    
                    // Generate new data point
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

                    // Draw a glitch line
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

                const handleResize = () => {
                    canvas.width = canvas.parentElement.clientWidth;
                    canvas.height = canvas.parentElement.clientHeight;
                };

                handleResize();
                window.addEventListener('resize', handleResize);
                draw();

                return () => {
                    window.removeEventListener('resize', handleResize);
                    cancelAnimationFrame(animationFrameId);
                };
            }, []);

            return <canvas ref={canvasRef} className="glowing-canvas" style={{ width: '100%', height: '100%', minHeight: '150px' }} />;
        }

        function TerminalSimulator({ onBootComplete }) {
            const [logs, setLogs] = useState([]);
            const [isBooting, setIsBooting] = useState(true);
            const logRef = useRef(null);

            useEffect(() => {
                const bootSequence = [
                    'INITIALIZING SYSTEM PROTOCOLS...',
                    'LOADING CYBER-CORE v7.1.2...',
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
                        setTimeout(() => setIsBooting(false), 1000);
                        setTimeout(onBootComplete, 1500);
                    }
                }, 300);
                
                return () => clearInterval(interval);
            }, []);

            useEffect(() => {
                if (logRef.current) {
                    logRef.current.scrollTop = logRef.current.scrollHeight;
                }
            }, [logs]);

            return (
                <div style={{ padding: '1rem', backgroundColor: 'rgba(0, 255, 192, 0.05)', border: '1px solid #00ffc0', borderRadius: '8px', height: '100%', display: isBooting ? 'flex' : 'none', flexDirection: 'column' }}>
                    <h2 style={{ fontFamily: 'Orbitron', fontSize: '1.25rem', marginBottom: '0.5rem', color: '#00ffc0' }}>SYSTEM_BOOT_SEQUENCE</h2>
                    <div ref={logRef} style={{ flexGrow: 1, overflowY: 'auto', whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontSize: '0.75rem' }}>
                        {logs.map((log, index) => <div key={index}>{log}</div>)}
                    </div>
                </div>
            );
        }

        function SystemControlTerminal() {
            const [history, setHistory] = useState(['Cyber-Core Command-Line Interface v7.1.2', 'Type "help" for a list of commands.', '>>']);
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
                            response = 'STATUS: ONLINE\nUPTIME: 7h 42m\nMODULES: 7/7 ACTIVE\nLOAD: 45%';
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
                            setHistory(['Cyber-Core Command-Line Interface v7.1.2', 'Type "help" for a list of commands.', '>>']);
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
                <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                    <div className="terminal-output scrollable-content" ref={terminalRef}>
                        {history.map((line, index) => <div key={index}>{line}</div>)}
                    </div>
                    <input
                        type="text"
                        className="terminal-input"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleCommand}
                        autoFocus
                    />
                </div>
            );
        }

        function StatusPanel({ title, value }) {
            return (
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                    <h2 style={{ fontSize: '1rem', marginBottom: '0.5rem', color: '#00ffc0' }}>{title}</h2>
                    <p style={{ fontSize: '1.5rem', textAlign: 'center', fontFamily: 'Orbitron' }}>{value}</p>
                </div>
            );
        }

        function BotInfoPanel({ info }) {
            return (
                <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'center' }}>
                    <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: '#00ffc0' }}>BOT_INFO</h2>
                    <p style={{ fontSize: '0.875rem', textAlign: 'center' }}>{info}</p>
                </div>
            );
        }

        function InviteBotPanel({ inviteUrl }) {
            return (
                <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'center' }}>
                    <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: '#00ffc0' }}>INVITE_BOT</h2>
                    <a href={inviteUrl} target="_blank" rel="noopener noreferrer" className="invite-button" style={{ marginTop: '1rem' }}>
                        INVITE BOT
                    </a>
                </div>
            );
        }

        function MainDashboard() {
            const [status, setStatus] = useState({
                uptime_formatted: '...',
                ping_ms: '...',
                load: 0,
                bot_info: 'Loading...',
                invite_url: '#'
            });

            useEffect(() => {
                const fetchStatus = async () => {
                    try {
                        const [statusResponse, loadResponse, infoResponse, inviteResponse] = await Promise.all([
                            fetch('/api/status'),
                            fetch('/api/load'),
                            fetch('/api/info'),
                            fetch('/api/invite')
                        ]);
                        const statusData = await statusResponse.json();
                        const loadData = await loadResponse.json();
                        const infoData = await infoResponse.json();
                        const inviteData = await inviteResponse.json();
                        
                        setStatus({
                            uptime_formatted: statusData.uptime_formatted,
                            ping_ms: statusData.ping_ms,
                            load: loadData.load,
                            bot_info: infoData.description,
                            invite_url: inviteData.url
                        });
                    } catch (error) {
                        console.error('Error fetching bot status:', error);
                    }
                };

                fetchStatus();
                const interval = setInterval(fetchStatus, 3000);
                return () => clearInterval(interval);
            }, []);

            return (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 1fr', gridTemplateRows: '1fr 1fr', gap: '1rem', height: '100%' }}>
                    <div className="data-panel" style={{ gridColumn: '1', gridRow: '1 / 3' }}>
                        <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: '#00ffc0' }}>NETWORK_VISUALIZER</h2>
                        <ParticleSystem systemLoad={status.load} />
                    </div>
                    <div className="data-panel" style={{ gridColumn: '2', gridRow: '1 / 2' }}>
                        <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: '#00ffc0' }}>DATA_STREAM</h2>
                        <DataWaveform />
                    </div>
                    <div className="data-panel" style={{ gridColumn: '2', gridRow: '2 / 3' }}>
                        <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: '#00ffc0' }}>SYSTEM_CONTROL</h2>
                        <SystemControlTerminal />
                    </div>
                    <div className="data-panel" style={{ gridColumn: '3', gridRow: '1 / 2', display: 'flex', flexDirection: 'column' }}>
                        <StatusPanel title="SYSTEM_UPTIME" value={status.uptime_formatted} />
                        <div style={{ height: '1px', backgroundColor: '#00ffc0', margin: '1rem 0' }} />
                        <StatusPanel title="SYSTEM_PING" value={status.ping_ms + "ms"} />
                    </div>
                    <div className="data-panel" style={{ gridColumn: '3', gridRow: '2 / 3' }}>
                        <BotInfoPanel info={status.bot_info} />
                        <div style={{ height: '1px', backgroundColor: '#00ffc0', margin: '1rem 0' }} />
                        <InviteBotPanel inviteUrl={status.invite_url} />
                    </div>
                </div>
            );
        }

        function App() {
            const [isBooted, setIsBooted] = useState(false);
            const handleBootComplete = () => setIsBooted(true);

            return (
                <div style={{ width: '100%', height: '100%' }}>
                    <div className="container">
                        <header className="header">
                            <div className="glitch-text" style={{ fontSize: '2rem' }}>CYBER-BOT // SYSTEM_STATUS</div>
                            <div style={{ fontSize: '0.875rem' }}>{isBooted ? 'ONLINE // OPERATIONAL' : 'BOOTING...'}</div>
                        </header>
                        <main style={{ gridColumn: '1 / -1', height: '100%' }}>
                            {isBooted ? <MainDashboard /> : <TerminalSimulator onBootComplete={handleBootComplete} />}
                        </main>
                    </div>
                </div>
            );
        }

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
"""

# ====================
# Web Server for Uptime Monitoring
# ====================

app = Flask(__name__)
command_usage = defaultdict(int)

@app.route('/api/load')
async def bot_load_api():
    return jsonify({
        'load': random.randint(20, 80)
    })

@app.route('/api/info')
async def bot_info_api():
    return jsonify({
        'description': 'This is a highly-advanced, self-monitoring AI construct designed to manage, secure, and interact with network environments. It is a fusion of a multi-modal perception core and an adaptive logic engine. Its primary directive is to maintain system integrity and provide advanced utility functions to its administrators.'
    })

@app.route('/api/invite')
async def bot_invite_api():
    invite_url = "https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot"
    return jsonify({
        'url': invite_url
    })

@app.route('/api/status')
async def bot_status_api():
    current_time = time.time()
    uptime_seconds = int(round(current_time - start_time))
    
    uptime_minutes = int(uptime_seconds / 60)
    uptime_hours = int(uptime_minutes / 60)
    remaining_minutes = uptime_minutes % 60
    remaining_seconds = uptime_seconds % 60
    uptime_formatted = f'{uptime_hours}h {remaining_minutes}m {remaining_seconds}s'

    try:
        ping_ms = round(bot.latency * 1000)
    except AttributeError:
        # This will happen if the bot is not yet ready, preventing a crash.
        ping_ms = 'N/A'

    return jsonify({
        'uptime_formatted': uptime_formatted,
        'ping_ms': ping_ms,
        'commands': [] # Commands list is no longer used in this version
    })

@app.route('/')
def home():
    return render_template_string(react_dashboard_html)

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ====================
# Discord Bot Setup
# ====================

TOKEN = os.environ.get("DISCORD_BOT_SECRET")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
start_time = time.time()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('Bot is ready and online!')
    await bot.change_presence(activity=discord.Game(name="Maintaining system integrity"))

@bot.command(help="Responds with a friendly greeting.")
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}! Acknowledging receipt.')

@bot.command(help="Responds with the bot's latency.")
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms. System is responsive.')

@bot.command(name='status', help="Reports the bot's uptime.")
async def bot_status(ctx):
    current_time = time.time()
    uptime_seconds = int(round(current_time - start_time))
    uptime_minutes = int(uptime_seconds / 60)
    uptime_hours = int(uptime_minutes / 60)
    remaining_minutes = uptime_minutes % 60
    remaining_seconds = uptime_seconds % 60
    await ctx.send(f"System has been operational for {uptime_hours}h {remaining_minutes}m {remaining_seconds}s. All systems nominal. ✅")


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    try:
        if TOKEN:
            bot.run(TOKEN)
        else:
            print("ERROR: Discord bot token not found in environment variables.")
    except discord.errors.LoginFailure as e:
        print(f"Error logging in: {e}")
        print("Please check your bot token.")
