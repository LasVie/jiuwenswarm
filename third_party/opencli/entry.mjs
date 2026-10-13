// Entry point of the bundled OpenCLI runtime.
//
// The desktop app runs OpenCLI with its own executable in Electron Node mode
// (ELECTRON_RUN_AS_NODE=1). Commander, OpenCLI's argv parser, detects Electron
// and, unless process.defaultApp is set, assumes a packaged app whose argv has
// no script path, so it would read this file's path as the command name.
// Marking the run as a default app restores Node's [execPath, script, ...args]
// layout. Under plain Node this is a no-op.
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

if (process.versions.electron) process.defaultApp = true;

const root = path.dirname(fileURLToPath(import.meta.url));
await import(pathToFileURL(path.join(root, 'node_modules', '@jackwener', 'opencli', 'dist', 'src', 'main.js')).href);
