# Video Demo Script — Loss Landscape: Why Skip Connections Matter

Duration target: ~2 minutes. Record your screen showing the visualization while reading this.

---

## [0:00 – 0:15] Introduction

> Hi, I'm [Your Name] and this is my EE508 extra-credit contribution: an interactive 3D loss landscape visualizer.
>
> This visualization demonstrates the key finding from Li et al.'s 2018 NeurIPS paper — that skip connections fundamentally change the geometry of the loss landscape, making optimization much easier.

**[Action: Show the page loaded with default settings — ResNet-56, skip connections ON]**

---

## [0:15 – 0:45] The Smooth Landscape (Skip Connections ON)

> Here we're looking at a ResNet-56 loss surface with skip connections enabled. Notice how smooth and bowl-shaped it is — there's essentially one clean path to the global minimum.
>
> Watch what happens when I drop 50 gradient-descent balls at random starting positions.

**[Action: Click "Drop Balls"]**

> Almost all of them roll smoothly to the center and turn green — that means they converged to the global minimum. The counter shows something like 45 out of 50 reached it. The landscape is so well-behaved that starting position barely matters.

**[Action: Let balls run for a few seconds, point at the counter]**

---

## [0:45 – 1:15] The Chaotic Landscape (Skip Connections OFF)

> Now watch the dramatic difference when I turn skip connections off — same 56-layer network, same optimizer, same learning rate.

**[Action: Toggle "Skip Connections" to OFF]**

> The surface completely changes. Instead of a smooth bowl, we see bumps and ridges — these are the Gaussian barriers that represent the local minima in the real loss landscape.
>
> Let me drop balls again.

**[Action: Click "Drop Balls"]**

> Now many balls get stuck — they turn red, trapped in local minima. The counter might show only 15 or 20 out of 50 converging. That's the core insight: without skip connections, most random initializations fail to find the global minimum.

---

## [1:15 – 1:35] Depth Makes It Worse

> It gets even worse with deeper networks. Let me switch to 110 layers, still with skip connections off.

**[Action: Click "110" in the depth selector, then "Drop Balls"]**

> The landscape is now dramatically more chaotic. Even fewer balls converge. This is exactly what Li et al. showed — depth without skip connections creates an optimization nightmare.
>
> But if I turn skip connections back on...

**[Action: Toggle skip connections ON]**

> ...the surface smooths out again, even at 110 layers. That's why ResNets work.

---

## [1:35 – 2:00] Interactive Features and Closing

> Students can also experiment with different optimizers — SGD, Momentum, and Adam — and adjust the learning rate to see how hyperparameters interact with landscape geometry.

**[Action: Briefly show optimizer dropdown, adjust LR slider]**

> The 2D contour view gives another perspective on the same data.

**[Action: Click "2D Contour" tab, then back to "3D Surface"]**

> This visualization makes the paper's qualitative finding quantitative and visceral. Within 30 seconds, any student can see why skip connections are essential for training deep networks.
>
> Thank you.

---

## Tips for Recording

- Use a screen recorder (OBS, built-in Windows Game Bar, or Mac QuickTime)
- Record at 1080p or higher
- Keep the browser window maximized
- Rotate the 3D view briefly to show the surface depth
- Pause for 2–3 seconds on the counter after each "Drop Balls" click
