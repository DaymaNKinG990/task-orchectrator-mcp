#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where this npm package is installed
const packageDir = path.resolve(__dirname, '..');
const pythonServerPath = path.join(packageDir, 'src', 'task_orchectrator_mcp', 'server.py');

// Check if Python server file exists
if (!fs.existsSync(pythonServerPath)) {
    console.error('❌ Python server file not found:', pythonServerPath);
    process.exit(1);
}

// Function to check if uv is available
function checkUv() {
    return new Promise((resolve) => {
        const uvCheck = spawn('uv', ['--version'], { stdio: 'pipe' });
        uvCheck.on('close', (code) => {
            resolve(code === 0);
        });
        uvCheck.on('error', () => {
            resolve(false);
        });
    });
}

// Function to install Python dependencies
async function installDependencies() {
    console.log('📦 Installing Python dependencies...');
    
    return new Promise((resolve, reject) => {
        const uvSync = spawn('uv', ['sync'], { 
            cwd: packageDir,
            stdio: 'inherit'
        });
        
        uvSync.on('close', (code) => {
            if (code === 0) {
                console.log('✅ Dependencies installed successfully');
                resolve();
            } else {
                reject(new Error(`Failed to install dependencies: ${code}`));
            }
        });
        
        uvSync.on('error', (err) => {
            reject(new Error(`Failed to run uv sync: ${err.message}`));
        });
    });
}

// Function to run the Python server
function runServer() {
    console.log('🚀 Starting Task Orchestrator MCP Server...');
    
    // Log environment variables for debugging
    console.log('Environment variables:');
    console.log('TRELLO_API_KEY:', process.env.TRELLO_API_KEY ? 'SET' : 'NOT SET');
    console.log('TRELLO_TOKEN:', process.env.TRELLO_TOKEN ? 'SET' : 'NOT SET');
    console.log('TRELLO_WORKING_BOARD_ID:', process.env.TRELLO_WORKING_BOARD_ID ? 'SET' : 'NOT SET');
    
    // Run the Python server directly instead of as a module to avoid import conflicts
    const serverProcess = spawn('uv', ['run', 'python', pythonServerPath], {
        cwd: packageDir,
        stdio: 'inherit',
        env: { 
            ...process.env,
            // Ensure these environment variables are explicitly passed
            TRELLO_API_KEY: process.env.TRELLO_API_KEY,
            TRELLO_TOKEN: process.env.TRELLO_TOKEN,
            TRELLO_WORKING_BOARD_ID: process.env.TRELLO_WORKING_BOARD_ID
        }
    });
    
    serverProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`❌ Server exited with code ${code}`);
            process.exit(code);
        }
    });
    
    serverProcess.on('error', (err) => {
        console.error('❌ Failed to start server:', err.message);
        process.exit(1);
    });
    
    // Handle process signals
    process.on('SIGINT', () => {
        console.log('\n🛑 Shutting down server...');
        serverProcess.kill('SIGINT');
    });
    
    process.on('SIGTERM', () => {
        console.log('\n🛑 Shutting down server...');
        serverProcess.kill('SIGTERM');
    });
}

// Main function
async function main() {
    try {
        // Check if uv is available
        const uvAvailable = await checkUv();
        if (!uvAvailable) {
            console.error('❌ uv is not installed. Please install uv first:');
            console.error('   pip install uv');
            process.exit(1);
        }
        
        // Install dependencies if needed
        try {
            await installDependencies();
        } catch (error) {
            console.error('❌ Failed to install dependencies:', error.message);
            process.exit(1);
        }
        
        // Run the server
        runServer();
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

// Run the main function
main(); 