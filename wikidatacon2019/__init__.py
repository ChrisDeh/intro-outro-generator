#!/usr/bin/python3

from renderlib import *
from schedulelib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://mobile.wikidatacon.org/conference.xml'

# For (really) too long titles
titlemap = {
    14: "Keynote",
}

def introFrames(args):
    # fade in title, persons and id
    frames = 2 * fps
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', easeOutQuart(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', 0),
        )

    frames = 2 * fps
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', easeOutQuart(i, 0, 1, frames)),
        )
    frames = 2 * fps
    for i in range(0, frames):
        yield (
            ('title', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
        )


def backgroundFrames(parameters):
    pass

def outroFrames(args):
    # fadein outro graphics
    frames = 1 * fps
    for i in range(0, frames):
        yield (
            ('fadetoblack', 'style', 'opacity', easeInQuart(i, 1, -1, frames)),
        )
    frames = 5 * fps
    for i in range(0, frames):
        yield []


def pauseFrames(args):
    pass

def debug():
#    render('intro.svg',
#           '../intro.ts',
#           introFrames,
#           {
#               '$id': 7776,
#               '$title': 'StageWar live!',
#               '$subtitle': '',
#               '$persons': 'www.stagewar.de'
#           }
#           )
#
    render('outro.svg',
           '../outro.ts',
           outroFrames
           )

def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl, titlemap):
        if not (idlist == []):
            if 000000 in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue
            if int(event['id']) not in idlist:
                print("skipping id (%s [%s])" % (event['title'], event['id']))
                continue
        if not event['room'] in ['Kleist', 'Kepler', 'Einstein']:
            continue

        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile='intro.svg',
            outfile=str(event['id']) + ".ts",
            sequence=introFrames,
            parameters={
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': '',
                '$persons': event['personnames']
            }
        ))

    # place a task for the outro into the queue
    if not "out" in skiplist:
        queue.put(Rendertask(
            infile='outro.svg',
            outfile='outro.ts',
            sequence=outroFrames
        ))

    # place the pause-sequence into the queue
    if not "pause" in skiplist:
        queue.put(Rendertask(
            infile='pause.svg',
            outfile='pause.ts',
            sequence=pauseFrames
        ))

    # place the background-sequence into the queue
    if not "bg" in skiplist:
        queue.put(Rendertask(
            infile='background.svg',
            outfile='background.ts',
            sequence=backgroundFrames
        ))
