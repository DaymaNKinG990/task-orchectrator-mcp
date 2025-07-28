const { spawn } = require('child_process');
const path = require('path');

console.log('🔧 Setting up Task Orchestrator MCP Server...');

const packageDir = path.resolve(__dirname, '..');

// Check if uv is available and install dependencies
const uvCheck = spawn('uv', ['--version'], { stdio: 'pipe' });

uvCheck.on('close', (code) => {
    if (code === 0) {
        console.log('📦 Installing Python dependencies...');
        
        const uvSync = spawn('uv', ['sync'], { 
            cwd: packageDir,
            stdio: 'inherit'
        });
        
        uvSync.on('close', (syncCode) => {
            if (syncCode === 0) {
                console.log('✅ Task Orchestrator MCP Server setup complete!');
            } else {
                console.warn('⚠️  Failed to install Python dependencies. You may need to run "uv sync" manually.');
            }
        });
        
        uvSync.on('error', (err) => {
            console.warn('⚠️  Could not run uv sync:', err.message);
        });
    } else {
        console.warn('⚠️  uv not found. Please install uv first: pip install uv');
        console.log('📋 After installing uv, run: uv sync');
    }
});

uvCheck.on('error', () => {
    console.warn('⚠️  uv not found. Please install uv first: pip install uv');
    console.log('📋 After installing uv, run: uv sync');
}); 