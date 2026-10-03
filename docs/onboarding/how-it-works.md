# How It Works

This page shows how the picture gets from the room to people watching at home. It also explains which parts you operate and which parts other people handle.

## Signal flow

The **signal flow** is the path the video takes, from the cameras to the viewer's screen.

<figure markdown="span">
  ![Cam 1 and Cam 2, moved by the SuperJoy, and ProPresenter Lyrics and Slides all feed Ecamm Live. The Stream Deck picks the Ecamm scene. Ecamm sends the program to Resi, which streams to YouTube and the church website.](../assets/diagrams/signal-flow.svg)
  <figcaption>How the picture gets from the room to viewers. Thick boxes are the parts you operate. Solid arrows carry video; dashed arrows only send commands.</figcaption>
</figure>

Read the picture from left to right:

1. **Four sources** send pictures into Ecamm Live. A **source** is anything that gives you a picture.
2. **Ecamm Live** is the software on the booth computer. It combines the sources into finished **scenes**, for example "Cam 1 with lyrics on top".
3. The **Stream Deck** is a small keypad with picture buttons. Each button picks one scene in Ecamm.
4. Whatever scene Ecamm shows right now is the **program**: the picture that goes out live. Ecamm sends the program to **Resi**.
5. **Resi** is the streaming service. It sends the program to **YouTube** and to the video player on the **church website**.

## The four sources

| Source | What it is | Who controls it |
|---|---|---|
| **Cam 1** | PTZOptics camera at the back center of the room | You, with the SuperJoy |
| **Cam 2** | PTZOptics camera on the left side when you face the stage | You, with the SuperJoy |
| **ProPresenter: Lyrics** | Song words, shown as a bar across the bottom of the screen | The ProPresenter operator |
| **ProPresenter: Slides** | Countdown, announcement slides, sermon slides | The ProPresenter operator |

A **PTZ camera** is a camera that a motor can pan (turn left or right), tilt (aim up or down) and zoom (get closer or wider). You never touch the camera itself. You move it from the booth with the **SuperJoy**, a joystick controller. Each camera has saved shots called **presets**, and one button on the SuperJoy recalls a preset. See [Cameras and Presets](cameras-and-presets.md).

ProPresenter runs on a separate computer, and another team operates it. You don't choose which lyric or slide appears. You only choose *whether* the lyrics or slides are part of the picture, by pressing a scene button.

## Who does what

| Who | Their job |
|---|---|
| **You, the livestream operator** | Move the cameras with the SuperJoy. Pick scenes with the Stream Deck. Start broadcasting in Ecamm before T-30. End the Resi stream after the service. Do the [post-production](../post-production.md) afterwards. |
| **ProPresenter operator** | Shows the right lyric or slide at the right time, in the room and on the stream. |
| **Audio team** | All sound. You don't adjust audio. If the sound is wrong, tell the audio team. |
| **On-call tech lead** | Helps when something breaks. Their contact details are on the private booth card. |
| **Livestream Lead** | Trains new operators, signs off the [Skills Checklist](../training/skills-checklist.md), and decides changes to presets and scenes. |

## When the stream starts and stops

"T-30" means 30 minutes before the service starts. "T-60" means 60 minutes before.

- **Resi starts by itself at T-30.** You don't press anything in Resi to start. Ecamm must already be broadcasting the Countdown scene by then, so Resi has a picture to send.
- **You end the Resi stream by hand, 5 minutes after the service ends.** Resi also has a 1-hour automatic end, but that is only a fallback for special events. Don't rely on it on a Sunday.

The full timeline is on the [Sunday Flow](sunday-flow.md) page.

## What you touch, and what you don't

| You use | You don't touch |
|---|---|
| SuperJoy (camera presets) | Audio mixer and sound settings |
| Stream Deck (scenes) | The ProPresenter computer |
| Ecamm Live (scene management) | Saved presets and scene layouts (the Livestream Lead changes these) |
| Resi (end the stream) | Camera menus and exposure settings |

!!! tip "Not sure who owns a problem?"
    Lyrics or slides wrong: tell the ProPresenter operator. Sound wrong: tell the audio team. Picture or stream wrong and you can't fix it with a scene button: call the on-call tech lead.
