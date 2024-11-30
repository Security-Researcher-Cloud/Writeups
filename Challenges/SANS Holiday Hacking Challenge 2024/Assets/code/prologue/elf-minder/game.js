const canvas = document.getElementById('gamecanvas');
const ctx = canvas.getContext('2d');

const levelId = new Chance().integer({ min: 100000000, max: 999999999 });
const chance = new Chance(levelId);
let chanceStable;

let worldStep = 0;

const rows = 5;
const cols = 7;
const cellSize = canvas.width / cols;
let collectedCrates = [];

const backgroundColors = [
    '#D2B48C', // 0: sand 1
    '#DEB887', // 1: sand 2
    'blue', // 2: water
    'black', // 3: hazard
];

const ImageAssets = {
    crate: 'crate.png',
    elf: 'elf.png',
    x: 'x.png',
};

let toLoad = Object.keys(ImageAssets).length;

Object.keys(ImageAssets).forEach(imageId => {
    const img = new Image();
    img.src = ImageAssets[imageId];
    ImageAssets[imageId] = img;
    img.onload = () => {
        toLoad--;
        if (toLoad === 0) {
            drawGrid();
            buildLevel();

            worldStep = 0;
            stepWorld();
        }
    };
});

const drawImageWithTransform = (img, x, y, rotation=0, xScale=1, yScale=1, origin={x: 0, y: 0}) => {
    ctx.save();  
    ctx.translate(x, y);
    ctx.rotate(rotation);
    ctx.scale(xScale, yScale); 
    ctx.drawImage(
      img, 
      -origin.x, 
      -origin.y, 
      img.width, 
      img.height
    );
    ctx.restore(); 
}

const __PARSE_URL_VARS__ = () => {
    let vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

const urlParams = __PARSE_URL_VARS__();

function getRandomSandColor() {
    return backgroundColors[chanceStable.bool() ? 0 : 1];
}

function drawGrid() {
    chanceStable = new Chance(levelId);
    ctx.strokeStyle = 'rgba(209,199,187,.4)'; // Grid color
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            if (i >= cols - 1) {
                ctx.fillStyle = 'blue';
            } else {
                ctx.fillStyle = getRandomSandColor();
            }
            ctx.fillRect(i * cellSize, j * cellSize, cellSize, cellSize);
            ctx.strokeRect(i * cellSize, j * cellSize, cellSize, cellSize);
        }
    }
}

const randomCrateLocation = () => ([
    chance.integer({ min: 0, max: 6 }),
    chance.integer({ min: 0, max: 6 }),
]);


function getRandomPath(cells) {
    const path = [];
    
    function addPathSegment(fromX, fromY, toX, toY) {
      let currentX = fromX;
      let currentY = fromY;
      
      while (currentX !== toX || currentY !== toY) {
        path.push([currentX, currentY, 1]);
        const directions = [];
        
        if (currentX < toX) directions.push([1, 0]);
        if (currentX > toX) directions.push([-1, 0]);
        if (currentY < toY) directions.push([0, 1]);
        if (currentY > toY) directions.push([0, -1]);
  
        const [dx, dy] = chance.pickone(directions);
        currentX += dx;
        currentY += dy;
      }
      path.push([toX, toY, 1]);
    }
  
    for (let i = 0; i < cells.length - 1; i++) {
      const [fromX, fromY] = cells[i];
      const [toX, toY] = cells[i + 1];
      addPathSegment(fromX, fromY, toX, toY);
    }
    
    // remove duplicates that are adjacent
    for (let i = 0; i < path.length - 1; i++) {
      if (path[i][0] === path[i + 1][0] && path[i][1] === path[i + 1][1]) {
        path.splice(i, 1);
        i--;
      }
    }

    return path;
  }
  

function drawPath(path) {    
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(path[0][0] * cellSize + cellSize / 2, path[0][1] * cellSize + cellSize / 2);
    
    for (let i = 1; i < path.length; i++) {
        ctx.lineTo(path[i][0] * cellSize + cellSize / 2, path[i][1] * cellSize + cellSize / 2);
    }
    
    ctx.stroke();
}

// drawGrid();

const getRandomCell = () => ([
    chance.integer({ min: 0, max: cols - 3}),
    chance.integer({ min: 0, max: rows - 2}),
]);


function drawDot(x, y, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(x * cellSize + cellSize / 2, y * cellSize + cellSize / 2, cellSize * .3, 0, 2 * Math.PI);
    ctx.fill();
}

const getHazard = path => {
    let cell = getRandomCell();
    // make sure cell isn't on path
    while (path.some(([x, y]) => x === cell[0] && y === cell[1])) {
        cell = getRandomCell();
    }
    return [...cell, 4];
};

const numHazardsByDifficulty = () => {
    const difficulty = urlParams.difficulty || 'easy';
    switch (difficulty) {
        case 'easy':
            return 2;
        case 'medium':
            return 4;
        case 'hard':
            return 8;
    }
}

const getHazards = (num, path) => {
    const hazards = [];
    
    for (let i = 0; i < numHazardsByDifficulty(); i++) {
        const hazard = getHazard(path);
        hazards.push(hazard);
    }
    return hazards;
}

const isCellInPath = (x, y, path) => {
    for (let i = 0; i < path.length; i++) {
        try {
            if (path[i][0] === x && path[i][1] === y) {
                return true;
            }
        } catch(e) {
            console.log(e);
        }
    }
    return false;
};

const getNumNeighborsInPath = (x, y, path) => {
    let num = 0;
    if (isCellInPath(x - 1, y, path)) num++;
    if (isCellInPath(x + 1, y, path)) num++;
    if (isCellInPath(x, y - 1, path)) num++;
    if (isCellInPath(x, y + 1, path)) num++;
    return num;
}

// getPathCellTypeByNumNeighbors
// one neighbor: cutback
// two neighbors on opposite sides: straight
// two or more neighbors on adjacent sides: bend

const getPathCellTypeByNumNeighbors = (x, y, path) => {
    const numNeighbors = getNumNeighborsInPath(x, y, path);
    if (numNeighbors === 1) return 'cutback';
    if (numNeighbors === 2) {
        if (isCellInPath(x - 1, y, path) && isCellInPath(x + 1, y, path)) {
            return 'straight';
        } else {
            return 'bend';
        }
    }
    return 'bend';
}

// strokeCellByType (outline entire cell with color based on type)
// cutback: red
// straight: blue
// bend: green

const strokeCellByType = (x, y, type, extra) => {
    // ctx.lineWidth = 3;
    // ctx.strokeStyle = 'black';
    // ctx.beginPath();
    // ctx.rect(x * cellSize, y * cellSize, cellSize, cellSize);
    // ctx.stroke();
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 1;
    ctx.fillStyle = 'white';
    ctx.font = '13px Arial';
    ctx.fillText(`${type}\n
${extra.join(',')}`, x * cellSize + 10, y * cellSize + 30);
}

const labelCellsByType = path => {
    for (let i = 0; i < path.length; i++) {
        const [x, y] = path[i];
        const type = getPathCellTypeByConnectionPoints(path[i]);
        strokeCellByType(x, y, type, path[i].slice(3));
    }
}

const getPathCellTypeByConnectionPoints = (cell) => {
    const [right, down, left, up] = cell.slice(3);

    if ((right && down) || (down && left) || (left && up) || (up && right)) return 'bend';
    if ((right && left) || (up && down)) return 'straight';
    return 'cutback';
}

const setConnectionPoints = path => {
    path.forEach((cell, i) => {
        cell.push(0, 0, 0, 0); // right (3), down (4), left (5), up (6)
    });
    path.forEach((cell, i) => {
        const [x, y] = cell;
        const nextCell = path[i + 1];
        if (nextCell) {
            const [nextX, nextY] = nextCell;
            if (nextX > x) {
                cell[3] = 1;
                nextCell[5] = 1;
            } else if (nextX < x) {
                cell[5] = 1;
                nextCell[3] = 1;
            } else if (nextY > y) {
                cell[4] = 1;
                nextCell[6] = 1;
            } else if (nextY < y) {
                cell[6] = 1;
                nextCell[4] = 1;
            }
        }
    });
};



const renderCell = cell => {
    const [x, y, type, right, down, left, up] = cell;
    switch(type) {
        case 1: // path
        case 2: // crate
        case 3: // control point
            ctx.save();
            ctx.beginPath();
            if (right) ctx.moveTo(x * cellSize + cellSize, y * cellSize + cellSize / 2);
            ctx.lineTo(x * cellSize + cellSize / 2, y * cellSize + cellSize / 2);

            if (down) ctx.moveTo(x * cellSize + cellSize / 2, y * cellSize + cellSize);
            ctx.lineTo(x * cellSize + cellSize / 2, y * cellSize + cellSize / 2);

            if (left) ctx.moveTo(x * cellSize, y * cellSize + cellSize / 2);
            ctx.lineTo(x * cellSize + cellSize / 2, y * cellSize + cellSize / 2);

            if (up) ctx.moveTo(x * cellSize + cellSize / 2, y * cellSize);
            ctx.lineTo(x * cellSize + cellSize / 2, y * cellSize + cellSize / 2);
            ctx.strokeStyle = 'green';
            ctx.setLineDash([10, 10]);
            ctx.lineWidth = 5;
            ctx.stroke();
            ctx.restore();

            if (type === 2 && !collectedCrates.find(c => c[0] === x && c[1] === y)) {
                drawImageWithTransform(ImageAssets.crate, x * cellSize + (cellSize - ImageAssets.crate.width) / 2, y * cellSize + (cellSize - ImageAssets.crate.height) / 2);
                // drawDot(x, y, 'brown');
            }
            // if (type === 3) {
            //     drawDot(x, y, 'yellow');
            // }
            break;
        case 4: // hazard
            drawDot(x, y, 'black')
            break;
    }
};

const positionDXY = {
    0: [.5, 0],
    1: [0, .5],
    2: [-.5, 0],
    3: [0, -.5],
    4: [0, 0],
};

const interpolateMultiplePoints = (points, progress) => {
    const numSegments = points.length - 1;
    const segment = Math.floor(progress * numSegments);
    const localProgress = (progress * numSegments) % 1;
    const [x1, y1] = points[segment];
    const [x2, y2] = points[segment + 1];
    const dx = x2 - x1;
    const dy = y2 - y1;
    return [x1 + dx * localProgress, y1 + dy * localProgress];
};

const renderHero = () => {
    const { cell, journey, progress } = hero;
    const [x, y, type, right, down, left, up] = cell;

    let elfCellX = x * cellSize + cellSize / 2;
    let elfCellY = (y) * cellSize + cellSize / 2;

    const points = journey.map(jIndex => ([ elfCellX + positionDXY[jIndex][0] * cellSize, elfCellY + positionDXY[jIndex][1] * cellSize ]));
    // console.log(points, progress);
    const [elfX, elfY] = interpolateMultiplePoints(points, progress);
    // console.log(elfX, elfY);
    let segment = progress < .5 ? 0 : 1;

    
    if (progress < .5) {
        // right (0), down (1), left (2), up (3), center (4)
        
        // const [dx1, dy1] = positionDXY[path[0]];
        // const [dx2, dy2] = positionDXY[path[1]];

        // elfX += (dx2 - dx1) * cellSize * progress * 2;
        // elfY += (dy2 - dy1) * cellSize * progress * 2;
    } else {
        // const [dx1, dy1] = positionDXY[path[1]];
        // const [dx2, dy2] = positionDXY[path[2]];

        // elfX += (dx2 - dx1) * cellSize * progress * 2;
        // elfY += (dy2 - dy1) * cellSize * progress * 2;
    }

    drawImageWithTransform(ImageAssets.elf, elfX - (cellSize - ImageAssets.elf.width) / 2, -40 + elfY - (cellSize - ImageAssets.elf.height) / 2);
    
    // ctx.fillStyle = 'red';
    // ctx.beginPath();
    // ctx.arc(elfX, elfY, cellSize * .1, 0, 2 * Math.PI);
    // ctx.fill();

    // console.log(elfX, elfY);
    const lastCell = path[path.length - 1];
    // console.log('last cell:', lastCell, path);
    // draw x.png on last cell

    drawImageWithTransform(ImageAssets.x, lastCell[0] * cellSize + (cellSize - ImageAssets.x.width) / 2, lastCell[1] * cellSize + (cellSize - ImageAssets.x.height) / 2);
};


const cullDuplicates = path => {
    path.forEach((cell, i) => {
        const [x, y] = cell;
        // console.log(cell);
        const dupes = path.filter((c, j) => c[0] === x && c[1] === y);
        if (dupes.length > 1) {
            console.log(dupes);
            if (dupes.find((dupe) => getPathCellTypeByConnectionPoints(dupe) === 'bend')) {
                const bendIndex = dupes.findIndex((dupe) => getPathCellTypeByConnectionPoints(dupe) === 'bend');
                dupes.filter((dupe, i) => i !== bendIndex)
                    .forEach(dupe => dupe[0] = -1);
            } else if (dupes.find((dupe) => getPathCellTypeByConnectionPoints(dupe) === 'straight')) {
                dupes.filter((dupe) => getPathCellTypeByConnectionPoints(dupe) !== 'straight')
                    .forEach(dupe => dupe[0] = -1);
                dupes.slice(1).forEach(dupe => dupe[0] = -1);
            }
        }
    });
    return path.filter(cell => cell[0] !== -1);
};

canvas.addEventListener('click', handleCellClick);

function handleCellClick(event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const cellX = Math.floor(x / cellSize);
    const cellY = Math.floor(y / cellSize);
    const cell = path.find(cell => cell[0] === cellX && cell[1] === cellY);
    console.log(cell);
    const isHeroInCell = hero.cell[0] === cellX && hero.cell[1] === cellY;
    if (cell && !isHeroInCell) {
        const cellCenterX = cellX * cellSize + cellSize / 2;
        const cellCenterY = cellY * cellSize + cellSize / 2;
        const cellTL = [cellX * cellSize, cellY * cellSize];
        console.log(cellCenterX, cellCenterY, cellTL    );
        const dx = ( x - cellCenterX ) / cellSize;
        const dy = ( y - cellCenterY ) / cellSize;
        const slope = dy / dx;

        console.log(dx, dy, slope);
        // const clickSideX = x < cellCenterX ? 'left' : 'right';
        // const clickSideY = y < cellCenterY ? 'top' : 'bottom';
        rotateCell(cell, dx, dy);
        render();
    }
}

const rotateCell = (cell, dx, dy) => {
    const [x, y, type, right, down, left, up] = cell;
    const slope = Math.abs(dy / dx);

    // quadrants:
    // [3][4]
    // [2][1]

    let quadrant; 
    if (dx > 0 && dy > 0) {
        quadrant = 1;
    } else if (dx < 0 && dy > 0) {
        quadrant = 2;
    } else if (dx < 0 && dy < 0) {
        quadrant = 3;
    } else {
        quadrant = 4;
    }
    console.log(quadrant);
    let newCell;
    const cellType = getPathCellTypeByConnectionPoints(cell);
    switch(cellType) {
        case 'cutback':
            switch(quadrant) {
                case 1:
                    newCell = slope <= 1 ? [x, y, type, 1, 0, 0, 0] : [x, y, type, 0, 1, 0, 0];
                    break;
                case 2:
                    newCell = slope <= 1 ? [x, y, type, 0, 0, 1, 0] : [x, y, type, 0, 1, 0, 0];
                    break;
                case 3:
                    newCell = slope <= 1 ? [x, y, type, 0, 0, 1, 0] : [x, y, type, 0, 0, 0, 1];
                    break;
                case 4:
                    newCell = slope <= 1 ? [x, y, type, 1, 0, 0, 0] : [x, y, type, 0, 0, 0, 1];
                    break;
            }
            break;
        case 'straight':
            newCell = [x, y, type, up, right, down, left];
            break;
        case 'bend':
            switch(quadrant) {
                case 1:
                    newCell = [x, y, type, 1, 1, 0, 0];
                    break;
                case 2:
                    newCell = [x, y, type, 0, 1, 1, 0];
                    break;
                case 3:
                    newCell = [x, y, type, 0, 0, 1, 1];
                    break;
                case 4:
                    newCell = [x, y, type, 1, 0, 0, 1];
                    break;
            }
            break;
    }
    
    cell[3] = newCell[3];
    cell[4] = newCell[4];
    cell[5] = newCell[5];
    cell[6] = newCell[6];
    return newCell;
}

let path;
let hazards;
let hero;

const getNumRotationsByDifficulty = difficulty => {
    switch (difficulty) {
        case 'easy':
            return 4;
        case 'medium':
            return 10;
        case 'hard':
            return 20;
    }
}

const scramblePath = path => {
    const difficulty = urlParams.difficulty || 'easy';
    const numRotations = getNumRotationsByDifficulty(difficulty);
    for (let i = 0; i < numRotations; i++) {
        const cell = chance.pickone(path.slice(1));
        for (let b = 0; b < chance.integer({ min: 1, max: 4 }); b++) {
            rotateCell(cell, chance.floating({ min: 0, max: 1 }) - .5, chance.floating({ min: 0, max: 1 }) - .5);
        }
    }
};

// const positionDXY = {
//     0: [.5, 0],
//     1: [0, .5],
//     2: [-.5, 0],
//     3: [0, -.5],
//     4: [0, 0],
// };

const calculateJourneys = cell => {
    const [x, y, type, right, down, left, up] = cell;
    const journeys = [];
    const cellType = getPathCellTypeByConnectionPoints(cell);
    switch(cellType) {
        case 'cutback':
            if (right) journeys.push([0, 4, 0]);
            if (down) journeys.push([1, 4, 1]);
            if (left) journeys.push([2, 4, 2]);
            if (up) journeys.push([3, 4, 3]);
            break;
        case 'straight':
            if (right && left) {
                journeys.push([0, 4, 2]);
                journeys.push([2, 4, 0]);
            }
            if (up && down) {
                journeys.push([1, 4, 3]);
                journeys.push([3, 4, 1]);
            }
            break;
        case 'bend':
            if (right && down) journeys.push([0, 4, 1]);
            if (right && down) journeys.push([1, 4, 0]);
            if (down && left) journeys.push([1, 4, 2]);
            if (down && left) journeys.push([2, 4, 1]);
            if (left && up) journeys.push([2, 4, 3]);
            if (left && up) journeys.push([3, 4, 2]);
            if (up && right) journeys.push([3, 4, 0]);
            if (up && right) journeys.push([0, 4, 3]);
            break;
    }
    return journeys;
};

const getNextCell = () => {
    const { journey, progress, cell } = hero;
    const [x, y, type, right, down, left, up] = cell;
    const lastStep = journey[journey.length - 1];
    
    let nextCell;

    switch(lastStep) {
        case 0:
            nextCell = path.find(c => c[0] === x + 1 && c[1] === y);
            break;
        case 1:
            nextCell = path.find(c => c[0] === x && c[1] === y + 1);
            break;
        case 2:
            nextCell = path.find(c => c[0] === x - 1 && c[1] === y);
            break;
        case 3:
            nextCell = path.find(c => c[0] === x && c[1] === y - 1);
            break;
    }
    console.log('next cell:', nextCell);
    if (nextCell) {
        const journeys = calculateJourneys(nextCell);
        let nextJourney;
        switch(lastStep) {
            case 0:
                nextJourney = journeys.find(j => j[0] === 2);
                break;
            case 1:
                nextJourney = journeys.find(j => j[0] === 3);
                break;
            case 2:
                nextJourney = journeys.find(j => j[0] === 0);
                break;
            case 3:
                nextJourney = journeys.find(j => j[0] === 1);
                break;
        }
        console.log('prev journey:', journey);
        console.log('next journey:', nextJourney);
        if (nextJourney) {
            hero.journey = nextJourney;
            hero.cell = nextCell;
            console.log('NEXT JOURNEY SET:', hero.journey);
        } else {
            hero.journey = calculateJourneys(cell).find(j => j[0] === lastStep);
        }
    } else {
        hero.journey = calculateJourneys(cell).find(j => j[0] === lastStep);
    }
};


const stepWorld = () => {
    if (!hero) {
        console.log('creating hero', calculateJourneys(path[0])[0]);
        hero = {
            cell: path[0],
            journey: calculateJourneys(path[0])[0], // right (0), down (1), left (2), up (3), center (4)
            progress: .5,
        };
    } else {
        hero.progress += .05;
console.log(hero.progress);
        if (hero.progress >= 1) {
            getNextCell();
            hero.progress = 0;
            // hero.journey = calculateJourneys(hero.cell)[0];
        } else if (Math.abs(hero.progress - .5) < .0001) {
            console.log('PROGRESS .5');
            console.log('HERO CELL:', hero.cell);
            if (hero.cell[2] === 2) {
                collectedCrates.push(hero.cell);
                console.log('COLLECTED CRATE', collectedCrates);
            }
        }
    }
    // console.log(hero);
    worldStep++;
    render();
    setTimeout(stepWorld, 100);
};

const getNumCratesByDifficulty = difficulty => {
    switch (difficulty) {
        case 'easy':
            return 1;
        case 'medium':
            return 2;
        case 'hard':
            return 4;
    }
}

const removeDuplicates = cells => {
    return cells.filter((cell, i) => cells.findIndex(c => c[0] === cell[0] && c[1] === cell[1]) === i);
}

const getCrateLocations = () => {
    const difficulty = urlParams.difficulty || 'easy';
    const numCrates = getNumCratesByDifficulty(difficulty);
    const crates = [];
    while (removeDuplicates(crates).length <= numCrates) {
        crates.push(getRandomCell());
    }
    return crates;
}

const buildLevel = () => {
    // const crateLocation = getRandomCell();
    const crateLocations = getCrateLocations();

    let controlPoint;
    controlPoint = getRandomCell();

    while (!crateLocations.find(cell => cell[0] === controlPoint[0] && cell[1] === controlPoint[1])) {
        controlPoint = getRandomCell();
    }

    const cells = [[cols - 2, 0], ...crateLocations, controlPoint, [cols - 2, rows - 1]]; // Example list of cells
    path = getRandomPath(cells);
    setConnectionPoints(path);
    cullDuplicates(path);

    crateLocations.forEach(crate => {
        path.find(cell => cell[0] === crate[0] && cell[1] === crate[1])[2] = 2;
    });
    // path.find(cell => cell[0] === crateLocation[0] && cell[1] === crateLocation[1])[2] = 2;
    path.find(cell => cell[0] === controlPoint[0] && cell[1] === controlPoint[1])[2] = 3;
   
    scramblePath(path);

    // drawDot(crateLocation[0], crateLocation[1], 'brown');
    // drawDot(controlPoint[0], controlPoint[1], 'yellow');

    hazards = getHazards(4, path);
    // hazards.forEach(hazard => drawDot(hazard[0], hazard[1], 'black'));
};

const render = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawGrid();
    // labelCellsByType(path);
    path.forEach(renderCell);
    hazards.forEach(renderCell);
    renderHero();
};




