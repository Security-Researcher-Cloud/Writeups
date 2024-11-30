class GameSolver {
    constructor() {
        this.EntityTypes = {
            START: 0,
            END: 1,
            CRATE: 2,
            BLOCKER: 3,
            HAZARD: 4,
            STEAM: 5,
            PORTAL: 6,
            SPRING: 7
        };
    }

    // Load level data
    loadLevel(levelName) {
        if (!Levels[levelName]) {
            throw new Error(`Level ${levelName} not found`);
        }

        return {
            entities: Levels[levelName].entities,
            segments: []
        };
    }

    // Helper: Get cell midpoint
    getCellMidpoint([x, y]) {
        // Assuming cells are represented in grid coordinates
        // Convert to midpoint for rotation logic
        return [x + 0.5, y + 0.5];
    }

    // Trigger rotation
    triggerRotation(cell) {
        const midpoint = this.getCellMidpoint(cell);
        console.log(`Rotating at midpoint: ${midpoint}`);
        // Dispatch a rotation event to the game engine
        const rotationEvent = new CustomEvent('rotate', { detail: { midpoint } });
        document.dispatchEvent(rotationEvent);
    }

    // Rotate all segments
    rotateSegments(segments) {
        segments.forEach(([start, end]) => {
            const cellMidpoint = [
                Math.floor((start[0] + end[0]) / 2),
                Math.floor((start[1] + end[1]) / 2)
            ];
            this.triggerRotation(cellMidpoint);
        });
    }
    // Trigger start button
    startGame() {
        const startButton = document.getElementById('startBtn');
        if (startButton) {
            startButton.click();
            console.log('Game started');
        } else {
            console.error('Start button not found');
        }
    }

    // Find valid moves from a position
    getValidMoves(pos, segments, entities) {
        const moves = [];
        const directions = [[0,1], [1,0], [0,-1], [-1,0]];
        
        for (const [dx, dy] of directions) {
            const newPos = [pos[0] + dx, pos[1] + dy];
            
            if (!this.isBlocked(newPos, entities)) {
                moves.push(newPos);
            }
        }
        
        return moves;
    }

    // Check if a position is blocked
    isBlocked(pos, entities) {
        return entities.some(entity => 
            entity[0] === pos[0] && 
            entity[1] === pos[1] && 
            (entity[2] === this.EntityTypes.BLOCKER || entity[2] === this.EntityTypes.HAZARD)
        );
    }

    // Find specific entity positions
    findEntities(entities, type) {
        return entities.filter(entity => entity[2] === type);
    }

    // Create a unique state key for visited positions
    createStateKey(pos, collectedCrates) {
        return `${pos[0]},${pos[1]},${[...collectedCrates].sort().join(':')}`;
    }

    // Check if a position has a crate
    hasCrate(pos, crates) {
        return crates.some(crate => crate[0] === pos[0] && crate[1] === pos[1]);
    }

    // Find a path between two points that avoids obstacles
    findPath(start, end, entities) {
        const queue = [{
            pos: start,
            path: [start]
        }];
        const visited = new Set();
        
        while (queue.length > 0) {
            const current = queue.shift();
            const posKey = `${current.pos[0]},${current.pos[1]}`;
            
            if (visited.has(posKey)) continue;
            visited.add(posKey);
            
            if (current.pos[0] === end[0] && current.pos[1] === end[1]) {
                return current.path;
            }
            
            const moves = this.getValidMoves(current.pos, [], entities);
            for (const move of moves) {
                const moveKey = `${move[0]},${move[1]}`;
                if (!visited.has(moveKey)) {
                    queue.push({
                        pos: move,
                        path: [...current.path, move]
                    });
                }
            }
        }
        
        return null;
    }

    // Convert positions to segments
    pathToSegments(path) {
        const segments = [];
        for (let i = 0; i < path.length - 1; i++) {
            segments.push([path[i], path[i + 1]]);
        }
        return segments;
    }

    // Solve a level
    solve(levelName) {
        const levelData = this.loadLevel(levelName);
        if (!levelData) {
            console.error('Failed to load level data');
            return null;
        }

        const { entities } = levelData;
        const startEntity = entities.find(e => e[2] === this.EntityTypes.START);
        const endEntity = entities.find(e => e[2] === this.EntityTypes.END);
        const crates = entities.filter(e => e[2] === this.EntityTypes.CRATE);

        if (!startEntity || !endEntity) {
            console.error('Missing start or end positions');
            return null;
        }

        const start = [startEntity[0], startEntity[1]];
        const end = [endEntity[0], endEntity[1]];
        let currentPosition = start;

        const pathSegments = [];
        for (const crate of crates) {
            const cratePos = [crate[0], crate[1]];
            const pathToCrate = this.findPath(currentPosition, cratePos, entities);

            if (!pathToCrate) {
                console.error(`Cannot find path to crate at ${cratePos}`);
                return null;
            }

            pathSegments.push(...this.pathToSegments(pathToCrate));
            currentPosition = cratePos;
        }

        const pathToEnd = this.findPath(currentPosition, end, entities);
        if (!pathToEnd) {
            console.error('Cannot find path to end');
            return null;
        }

        pathSegments.push(...this.pathToSegments(pathToEnd));
        this.rotateSegments(pathSegments);

        const startBtn = document.getElementById('startBtn');
        if (startBtn) {
            startBtn.click();
            console.log('Game started');
        }

        return {
            segments: pathSegments,
            entities
        };
    }

    // Solve all levels
    solveAllLevels() {
        const results = {
            solved: [],
            failed: []
        };

        for (const levelName in Levels) {
            console.log(`\n=== Attempting level: ${levelName} ===`);
            try {
                const solution = this.solve(levelName);
                if (solution) {
                    localStorage.setItem(`level_${levelName}`, JSON.stringify(solution));
                    console.log(`✓ Solved ${levelName}`);
                    results.solved.push(levelName);
                } else {
                    console.log(`✗ Failed to solve ${levelName}`);
                    results.failed.push(levelName);
                }
            } catch (error) {
                console.error(`Error solving ${levelName}:`, error);
                results.failed.push(levelName);
            }
        }

        return results;
    }
}

// Run solver on all levels
try {
    const solver = new GameSolver();
    console.log('Starting solver for all levels...');
    const results = solver.solveAllLevels();
    
    console.log('\n=== Final Results ===');
    console.log(`Solved ${results.solved.length} levels:`, results.solved);
    console.log(`Failed ${results.failed.length} levels:`, results.failed);
} catch (error) {
    console.error('Solver error:', error);
}