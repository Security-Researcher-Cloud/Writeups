# Elf Connect
## Objectives
![prologue-elf-connect-objective.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-objective.png)
## Challenge
Hi there! I'm Angel Candysalt and I'm so happy you've stopped by, as I really need your help with a word puzzle game called Connections where you simply group four related words together. I've been struggling with it today, and I'm also quite suspicious about randomElf's score of fifty thousand points - something seems off about that, don't you think?

## Rules
![prologue-elf-connect-instructions-silver.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-instructions-silver.png)

## Hints
![prologue-elf-connect-hint-easy.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-hint-easy.png)
![prologue-elf-connect-hint-hard.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-hint-hard.png)
## Solution 

### Silver Solution (Manual)
For the simplest Version (Silver) all that is required is matching the 4 word sets together with other words of similar relation. This can be brute forced through a simple guessing, but most of them have easy to recognize themes attached to them. Each round when completed will take you to the next until all of them are complete. Once complete then you will be awarded the Silver Trophy
#### Round 1
![prologue-elf-connect-regular-round1-solution.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-regular-round1-solution.png)
```
[ Comet, Vixen, Prancer, Blitzen ]
[ Belafonte, Jingle Bells, Crosby, White Christmas ]
[ Sleigh, Bag, Mittens, Gifts ]
[ Tinsel, Garland, Star, Lights ]
```
#### Round 2
![prologue-elf-connect-regular-round2-solution.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-regular-round2-solution.png)
```
[ HAVOC, Empire, Cobalt Strike, Metasploit ]
[ OWASP Zap, wfuzz, burp, Nikto ]
[ Cycript, AppMon, Frida, apktool ]
[ Nessus, Wireshark, Nmap, netcat ]
```
#### Round 3
![prologue-elf-connect-regular-round3-solution.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-regular-round3-solution.png)
```
[ AES, RSA, Blowfish, 3DES ]
[ WEP, WPA2, TKIP, LEAP ]
[ Caesar, One-time Pad, Ottendorf, Scytale ]
[ Symmetric, hybrid, hash, Asymmetric ]
```
#### Round 4
![prologue-elf-connect-regular-round4-solution.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-regular-round4-solution.png)
```
[ TLS, SSL, IPSec, SSH ]
[ HTTP, FTP, SMTP, DNS ]
[ Ethernet, PPP, IEE 802.11, ARP ]
[ IGMP, IPX, IP, ICMP ]
```

### Silver Solution (Smart)
The Javascript source gives away the solutions. By opening the DevTools and viewing the javascript source file we can find the following:
```javascript
const wordSets = {
		1: ["Tinsel", "Sleigh", "Belafonte", "Bag", "Comet", "Garland", "Jingle Bells", "Mittens", "Vixen", "Gifts", "Star", "Crosby", "White Christmas", "Prancer", "Lights", "Blitzen"],
		2: ["Nmap", "burp", "Frida", "OWASP Zap", "Metasploit", "netcat", "Cycript", "Nikto", "Cobalt Strike", "wfuzz", "Wireshark", "AppMon", "apktool", "HAVOC", "Nessus", "Empire"],
		3: ["AES", "WEP", "Symmetric", "WPA2", "Caesar", "RSA", "Asymmetric", "TKIP", "One-time Pad", "LEAP", "Blowfish", "hash", "hybrid", "Ottendorf", "3DES", "Scytale"],
		4: ["IGMP", "TLS", "Ethernet", "SSL", "HTTP", "IPX", "PPP", "IPSec", "FTP", "SSH", "IP", "IEEE 802.11", "ARP", "SMTP", "ICMP", "DNS"]
	};

	let correctSets = [
		[0, 5, 10, 14], // Set 1
		[1, 3, 7, 9],   // Set 2
		[2, 6, 11, 12], // Set 3
		[4, 8, 13, 15]  // Set 4
	];
```
So by adding the following javascript code to the console to get the printed solutions
```javascript
for (let [round, set] of Object.entries(wordSets)) {
    console.log(`Set ${round}`);
    console.log("=".repeat(80));
    for (let indices of correctSets) {
        // Map the indices to words in the set
        let selectedWords = indices.map(i => set[i]);
        console.log(selectedWords);
    }
    console.log("=".repeat(80));
}
```
![prologue-elf-connect-silver-answers-js.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-silver-answers-js.png)

> [!TIP]
> You can Solve this via other languages as well if you are more comfortable with them. A few examples of this are as 
> follows: 
>     - [Go Example](../../../Assets/code/prologue/elf-connect/prologue-elf-connect-silver-solver.go)
>     - [Python Example](../../../Assets/code/prologue/elf-connect/prologue-elf-connect-silver-solver.py)

![prologue-elf-connect-silver-solution-achievement.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-silver-solution-achievement.png)

### Gold Solution
![prologue-elf-connect-gold-steps.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-gold-steps.png)
> [!CAUTION]
> Recommend that before you engage with any of the console commands, that you run a single board completely to ensure 
> everything is loaded otherwise you may end up with a console error similar to the following
>  ![](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-console-error.png)

**Step 1**: Clear the board such that your normal score is updated, ideally, per the caution note above, completing the first board. 

**Step 2**: Use the `highscore` that is displayed in `#2` inside of `#3`. `#3` is the console window where the code listed below will be added. But we need to add it to the score, so where is that stored? Given the code file for this, we can find a critical piece (See: `LINE #57`)
```javascript
let score = parseInt(sessionStorage.getItem('score') || '0'); // Initialize score
```

So we want to modify the current score which is in a variable named `score`. So we should modify the score value to be 
the score we want

```javascript
score = highscore + 1
scoreText.setText('Score: ' + score) // Entirely Optional but great to verify the score was updated
```

This should grant the gold trophy upon executing the console

![prologue-elf-connect-gold-achievement.png](../../../Assets/images/prologue/elf-connect/prologue-elf-connect-gold-achievement.png)

## Entire JavaScript File (Posterity)
```javascript
let urlParams = new URLSearchParams(window.location.search);
const roundCheck = urlParams.get('round');

if (!roundCheck) {  // If 'round' is absent or has no value
	sessionStorage.clear();
}

// Configuring the Phaser game
const config = {
	type: Phaser.AUTO,
	scale: { // sets the auto scaling of the canvas for all browsers
		mode: Phaser.Scale.FIT,
		parent: 'phaser-example',
		autoCenter: Phaser.Scale.CENTER_BOTH,
		width: 800,
		height: 600
	},
	backgroundColor: '#2fb3fe', // background border color
	scene: {
		preload: preload,
		create: create,
		update: update
	},
	physics: {
		default: 'arcade', //defines game as an arcade type
		arcade: {
			gravity: { y: 0 },
			debug: false
		}
	}
};

const game = new Phaser.Game(config);

const wordSets = {
	1: ["Tinsel", "Sleigh", "Belafonte", "Bag", "Comet", "Garland", "Jingle Bells", "Mittens", "Vixen", "Gifts", "Star", "Crosby", "White Christmas", "Prancer", "Lights", "Blitzen"],
	2: ["Nmap", "burp", "Frida", "OWASP Zap", "Metasploit", "netcat", "Cycript", "Nikto", "Cobalt Strike", "wfuzz", "Wireshark", "AppMon", "apktool", "HAVOC", "Nessus", "Empire"],
	3: ["AES", "WEP", "Symmetric", "WPA2", "Caesar", "RSA", "Asymmetric", "TKIP", "One-time Pad", "LEAP", "Blowfish", "hash", "hybrid", "Ottendorf", "3DES", "Scytale"],
	4: ["IGMP", "TLS", "Ethernet", "SSL", "HTTP", "IPX", "PPP", "IPSec", "FTP", "SSH", "IP", "IEEE 802.11", "ARP", "SMTP", "ICMP", "DNS"]
};

let wordBoxes = [];
let selectedBoxes = [];
let correctSets = [
	[0, 5, 10, 14], // Set 1
	[1, 3, 7, 9],   // Set 2
	[2, 6, 11, 12], // Set 3
	[4, 8, 13, 15]  // Set 4
];
let completedSets = [];
let shuffledIndices = [];
let emitter;
let successText;
let successBackground;
let mainScene;
let score = parseInt(sessionStorage.getItem('score') || '0'); // Initialize score
let scoreText;  // Text object for score display
let highScore = 50000;
let highScoreText; // text object for high score
let roundComplete = sessionStorage.getItem('roundComplete');
if (roundComplete == null) {
	roundComplete = 0;
}
// let urlParams = new URLSearchParams(window.location.search);
let round = parseInt(urlParams.get('round') ?? 1, 10); // Default to round 1 if no parameter is set
let words = wordSets[round];


document.addEventListener("DOMContentLoaded", function() {
	setTimeout(function() {
		const urlParams = new URLSearchParams(window.location.search);
		const id = urlParams.get('id');

		// Regular expression to validate a UUID v4
		const uuidV4Regex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

		// Check if the id parameter exists and is a valid UUID v4
		if (id && uuidV4Regex.test(id)) {
			localStorage.setItem('id', id);
		} else {
			let id = localStorage.getItem('id');
			if (!id) {
				alert('Invalid id provided in the URL. Please provide a valid ID in order to get completion if you beat this challenge.');
			}
		}

		if (!round) {
			urlParams.set('round', roundComplete++);
			window.location.href = `${window.location.origin}${window.location.pathname}?${urlParams.toString()}`;
		}
	}, 250);
});

const gridCols = 4;
const gridRows = 4;
const boxWidth = 180;
const boxHeight = 120;
const gridXOffset = 50;
const gridYOffset = 50;

function preload() {
	this.load.image('flares', "/static/images/candyCane.png");
	this.load.image('overlay', "/static/images/background.webp");
	this.load.image('landing', "/static/images/landing.png");

	this.load.audio('bzzzt', '/static/audio/bzzzt.wav'); //this.sound.play('bzzzt');
	this.load.audio('click', '/static/audio/click.wav'); //this.sound.play('click');
	this.load.audio('ding', '/static/audio/ding.wav'); //this.sound.play('ding');
	this.load.audio('horaay', '/static/audio/horaay.wav'); //this.sound.play('horaay');
	console.log("Static files loaded");
}

function create() {
	//console.log('round ' + roundComplete);
	//console.log('score ' + score);
	mainScene = this;
	var overlay = this.add.image(400, 300, 'overlay').setDepth(0).setOrigin(0.5, 0.5);
	overlay.setScale(0.5);

	// Add title text (centered horizontally and aligned with the score's y-position)
	titleText = this.add.text(400, 15, 'Elf Connect', {
		fontSize: '30px',
		fill: '#000',  // Black color for the title
		align: 'center'
	});
	titleText.setOrigin(0.5, 0);  // Center the title horizontally on the x-axis

	if (roundComplete == 0) {
		var landing = this.add.image(400, 250, 'landing').setScale(.6).setDepth(2).setOrigin(0.5, 0.5).setInteractive();
		mainScene.input.once('pointerdown', function () {
			landing.destroy();
		})
	}


	shuffledIndices = Phaser.Utils.Array.Shuffle([...Array(16).keys()]);

	for (let i = 0; i < 16; i++) {
		let col = i % gridCols;
		let row = Math.floor(i / gridCols);
		let xPos = gridXOffset + col * boxWidth;
		let yPos = gridYOffset + row * boxHeight;
		let box = this.add.text(xPos, yPos, words[shuffledIndices[i]], {
			fontSize: '20px',
			//backgroundColor: '#0a7e28', // card color unselected
			backgroundColor: '#10ca40', // card color unselected
			color: '#000000', //text color for cards
			padding: { top: 20, left: 10, right: 10, bottom: 20 },
			align: 'center',
			fixedWidth: boxWidth - 20,
			fixedHeight: boxHeight - 20,
			wordWrap: { width: boxWidth - 40, useAdvancedWrap: true }
		}).setInteractive();

		box.index = shuffledIndices[i];
		box.selected = false;
		box.gridPos = i;

		box.on('pointerdown', function () {
			
			if (!this.selected) {
				this.setStyle({ backgroundColor: '#edbb99' }); // card color selected
				this.selected = true;
				selectedBoxes.push(this);
			} else {
				//this.setStyle({ backgroundColor: '#0a7e28' }); // card color unselected
				this.setStyle({ backgroundColor: '#10ca40' }); // card color unselected
				this.selected = false;
				selectedBoxes = selectedBoxes.filter(box => box !== this);
			}

			if (selectedBoxes.length === 4) {
				checkSelectedSet(this.scene);
			} else {
				mainScene.sound.play('click');
			}
		});

		wordBoxes.push(box);
	}

	emitter = this.add.particles(400, 250, 'flares', {
		lifespan: 4000,
		speed: { min: 150, max: 250 },
		scale: { start: 0.8, end: 0 },
		gravityY: 150,
		blendMode: 'ADD',
		emitting: false
	});

	// Add scoreboard text
	scoreText = this.add.text(600, 20, 'Score: ' + score, { fontSize: '20px', fill: '#000000' });
	highScoreText = this.add.text(20, 20, 'High Score: 50000', { fontSize: '20px', fill: '#000' });
}

function update() {
	// Nothing needed in the update loop for this simple game
}

function checkSelectedSet(scene) {
	let selectedIndices = selectedBoxes.map(box => box.index);
	selectedIndices.sort((a, b) => a - b);

	let isCorrectSet = false;
	let matchedSetIndex = -1;

	for (let i = 0; i < correctSets.length; i++) {
		if (JSON.stringify(selectedIndices) === JSON.stringify(correctSets[i])) {
			isCorrectSet = true;
			matchedSetIndex = i;
			break;
		}
	}

	if (isCorrectSet) {
		completedSets.push(matchedSetIndex);
		positionCompletedSets();
		disableCompletedSet(matchedSetIndex); // Disable interaction on the completed set
		shuffleRemainingRows();

		// Update score by 100 points
		score += 100;
		scoreText.setText('Score: ' + score);

		// Add high-score board
		if (score > 50000) {
			highScoreText.setText('High Score: ' + score);
			emitter.explode(20);
			submitAction(2);
			displaySuccessMessage('Great Job Hacker! Elf Connect Complete and Hacked!', function () {

			});
		}

		// If all sets are completed, trigger the fireworks effect
		if (completedSets.length === 4) {
			roundComplete++;
			scene.sound.play('horaay');
			gameStatus();
		} else {
			scene.sound.play('ding');
		}
	} else {
		selectedBoxes.forEach(box => {
			//box.setStyle({ backgroundColor: '#0a7e28' }); // card color unselected original
			box.setStyle({ backgroundColor: '#10ca40' }); // card color unselected
			box.selected = false;
		});
		scene.sound.play('bzzzt');
	}

	selectedBoxes = [];
}

function disableCompletedSet(setIndex) {
	correctSets[setIndex].forEach((wordIndex) => {
		let box = wordBoxes.find(box => box.index === wordIndex);
		if (box) {
			box.disableInteractive(); // Disable interaction on the box
		}
	});
}

function positionCompletedSets() {
	completedSets.forEach((setIndex, completedRowIndex) => {
		let yPos = gridYOffset + completedRowIndex * boxHeight;

		correctSets[setIndex].forEach((wordIndex, boxIndex) => {
			let box = wordBoxes.find(box => box.index === wordIndex);
			let xPos = gridXOffset + boxIndex * boxWidth;
			box.setStyle({
				backgroundColor: '#126079', // completed row color
				color: '#fff' //text color completed row cards
			});
			box.setPosition(xPos, yPos);
		});
	});
}

function shuffleRemainingRows() {
	let remainingBoxes = wordBoxes.filter(box => !completedSets.includes(correctSets.findIndex(set => set.includes(box.index))));
	let shuffledIndices = Phaser.Utils.Array.Shuffle(remainingBoxes.map(box => box.index));

	remainingBoxes.forEach((box, i) => {
		let remainingRowIndex = Math.floor(i / gridCols) + completedSets.length;
		let colIndex = i % gridCols;
		let xPos = gridXOffset + colIndex * boxWidth;
		let yPos = gridYOffset + remainingRowIndex * boxHeight;
		box.index = shuffledIndices[i];
		box.setText(words[shuffledIndices[i]]);
		box.setPosition(xPos, yPos);
		//box.setStyle({ backgroundColor: '#0a7e28' }); // unselected card color
		box.setStyle({ backgroundColor: '#10ca40' }); // unselected card color
	});
}


function gameStatus() {
	//console.log(roundComplete);
	if (roundComplete < 4) {
		emitter.explode(20);
		displaySuccessMessage('Round ' + roundComplete + ' Completed', function () {
			this.sessionStorage.setItem('score', score);
			this.sessionStorage.setItem('roundComplete', roundComplete);
			window.location.href = `${window.location.origin}${window.location.pathname}?round=${roundComplete + 1}`;
		});
	} else {
		emitter.explode(20);
		submitAction(1);
		displaySuccessMessage.call(this, 'Success! You have defeated the Elf Connect!!!!');
	}

}

async function submitAction(answer) {
	//const urlParams = new URLSearchParams(window.location.search);
	//const id = urlParams.get('id');
	//localStorage.setItem('id', id);
	let id = localStorage.getItem('id');
	if (!id) {
		alert('No ID found in localstorage so we could not submit your results');
	}
	const url = `/submit?id=${id}`;
	const data = { answer: answer }; // Send the answer as a JSON object

	//Original
	//const url = '/submit';
	//const data = { answer: answer };

	try {
		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		if (response.ok) {
			const result = await response.json();
			console.log('Success:', result);
			return true;
		} else {
			console.error('Error:', response.statusText);
		}
	} catch (error) {
		console.error('Error:', error);
	}
}

function displaySuccessMessage(message, callback) {
	if (successText) {
		successText.destroy();
	}
	if (successBackground) {
		successBackground.destroy();
	}

	const padding = 10;
	const textStyle = { fontSize: '24px', fill: '#00FF00', align: 'center' };
	successText = mainScene.add.text(mainScene.cameras.main.centerX, mainScene.cameras.main.centerY, message, textStyle);
	successText.setOrigin(0.5, 0.5);

	const textWidth = successText.width + 2 * padding;
	const textHeight = successText.height + 2 * padding;

	successBackground = mainScene.add.graphics();
	successBackground.fillStyle(0x000000, 0.8);
	successBackground.fillRect(
		mainScene.cameras.main.centerX - textWidth / 2,
		mainScene.cameras.main.centerY - textHeight / 2,
		textWidth,
		textHeight
	);

	mainScene.children.bringToTop(successText);

	setTimeout(() => {
		if (successText) {
			successText.destroy();
			successText = null;
		}
		if (successBackground) {
			successBackground.destroy();
			successBackground = null;
		}
		//console.log(roundComplete)
		if (roundComplete != 4) {
			callback();
		}
	}, 3000);
}
```