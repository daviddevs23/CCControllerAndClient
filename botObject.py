class Bot:
    def __init__(self, websocket):
        self.websocket = websocket
        self.currX = 0      # +x = forward, -x = backward
        self.currY = 0      # +y = right, -y = left
        self.currZ = 0      # +z = up, -z = down
        self.currDirection = "forward" # What direction: forward, backward, left, right

        # Saving position so that you can return to that postion after refueing,
        # emptying inventory, etc..
        self.lastX = 0
        self.lastY = 0
        self.lastZ = 0
        self.lastDirection = "forward"

    async def stop(self):
        await self.websocket.send("stop")

    async def forward(self, distance=1):
        for i in range(distance):
            await self.websocket.send("forward")
            res = await self.websocket.recv()
            if res == "true":
                if self.currDirection == "backward":
                    self.currX -= 1

                elif self.currDirection == "forward":
                    self.currX += 1

                elif self.currDirection == "left":
                    self.currY -= 1

                elif self.currDirection == "right":
                    self.currY += 1

            return res

    async def back(self, distance=1):
        for i in range(distance):
            await self.websocket.send("back")
            res = await self.websocket.recv()
            if res == "true":
                if self.currDirection == "backward":
                    self.currX += 1

                elif self.currDirection == "forward":
                    self.currX -= 1

                elif self.currDirection == "left":
                    self.currY += 1

                elif self.currDirection == "right":
                    self.currY -= 1

            return res

    async def up(self, distance=1):
        for i in range(distance):
            await self.websocket.send("up")
            res = await self.websocket.recv()
            if res == "true":
                self.currZ += 1
                
            return res

    async def down(self, distance=1):
        for i in range(distance):
            await self.websocket.send("down")
            res = await self.websocket.recv()
            if res == "true":
                self.currZ -= 1
            
            return res
    
    async def fuelLevel(self):
        await self.websocket.send("fuelLevel")
        return await self.websocket.recv()

    async def refuel(self):
        await self.websocket.send("refuel")
        return await self.websocket.recv()

    async def digUp(self):
        await self.websocket.send("digUp")
        return await self.websocket.recv()

    async def digDown(self):
        await self.websocket.send("digDown")
        return await self.websocket.recv()

    async def dig(self):
        await self.websocket.send("dig")
        return await self.websocket.recv()

    async def right(self):
        await self.websocket.send("right")
        res = await self.websocket.recv()
        if res == "true":
            # Just plug in your current direction and get your new direction out
            dirDict = {"forward":"right", "backward":"left", "left":"forward", "right":"backward"}
            self.currDirection = dirDict[self.currDirection]

        return res

    async def left(self):
        await self.websocket.send("left")
        res = await self.websocket.recv()
        if res == "true":
            # Just plug in your current direction and get your new direction out
            dirDict = {"forward":"left", "backward":"right", "left":"backward", "right":"forward"}
            self.currDirection = dirDict[self.currDirection]

        return res

    async def place(self):
        await self.websocket.send("place")
        return await self.websocket.recv()

    async def placeUp(self):
        await self.websocket.send("placeUp")
        return await self.websocket.recv()

    async def placeDown(self):
        await self.websocket.send("placeDown")
        return await self.websocket.recv()
    
    async def fullSpaces(self):
        await self.websocket.send("fullSpaces")
        return await self.websocket.recv()

    async def getInventory(self):
        await self.websocket.send("getInventory")
        return await self.websocket.recv()

    async def currentSlot(self):
        await self.websocket.send("currentSlot")
        return await self.websocket.recv()
    
    async def pickSlot(self, slot):
        await self.websocket.send("pickSlot")
        await self.websocket.recv()
        await self.websocket.send(f"{slot}")
        return await self.websocket.recv()

    async def emptyAll(self):
        await self.websocket.send("emptyAll")
        return await self.websocket.recv()

    async def grabFuel(self):
        await self.websocket.send("grabFuel")
        return await self.websocket.recv()

    # Command that makes the bot go to a coordinate and face that direction
    async def gotTo(self, x, y, z, direction):
        self.lastDirection = self.currDirection
        self.lastX = self.currX
        self.lastY = self.currY
        self.lastZ = self.currZ

        # Get the disctance that we are from each desired point
        deltaX = abs(x - self.currX)
        deltaY = abs(y - self.currY)
        deltaZ = abs(z - self.currZ)

        # Go halfway through x
        halfDeltaX = deltaX // 2
        
        if self.currX > x:
            while self.currDirection != "backward":
                await self.right()

        else:
            while self.currDirection != "forward":
                await self.right()

        await self.forward(halfDeltaX)

        # Align Z
        while self.currZ != z:
            if self.currZ > z:
                await self.down()
            else:
                await self.up()

        # Align Y
        if y >= 0:
            if self.currDirection == "forward":
                if self.currY < y:
                    while self.currDirection != "left":
                        await self.left()

                else:
                    while self.currDirection != "right":
                        await self.left()

            elif self.currDirection == "backward":
                if self.currY < y:
                    while self.currDirection != "right":
                        await self.left()

                else:
                    while self.currDirection != "left":
                        await self.left()

        else:
            if self.currDirection == "forward":
                if self.currY > y:
                    while self.currDirection != "left":
                        await self.left()

                else:
                    while self.currDirection != "right":
                        await self.left()

            elif self.currDirection == "backward":
                if self.currY > y:
                    while self.currDirection != "right":
                        await self.left()

                else:
                    while self.currDirection != "left":
                        await self.left()


        while self.currY != y:
            await self.forward()

        # Realign direction
        if self.currX > x:
            while self.currDirection != "backward":
                await self.right()

        else:
            while self.currDirection != "forward":
                await self.right()

        # Rest of the way through x
        while self.currX != x:
            await self.forward()

        # Set final direction
        while self.currDirection != direction:
            await self.right()




    # Digs out a cub of the given size
    async def clearSpace(self, width, height, depth):
        
        for i in range(depth):
            if i != depth:
                await self.dig()
                await self.forward()

            await self.left()

            for j in range(height):
                await self.checkRefuel()
                await self.checkInventoryFull()

                for k in range(width - 1):
                    await self.dig()
                    await self.forward()

                await self.right()
                await self.right()

                if j != height - 1:
                    await self.digUp()
                    await self.up()
            
            # Return to original height
            for i in range(height):
                await self.down()

            # If even, just turn right
            if height % 2 == 0:
                await self.right()

            # If it is odd, return to point
            else:
                for i in range(width):
                    await self.forward()

                await self.left()

        await self.gotTo(0, 0, 0, "forward")


    # Checks if the inventory needs to be refilled and then refills it
    async def checkInventoryRefill(self):
        pass

    # Checks if the fuel is too low and then refills it
    async def checkRefuel(self):
        fuel = await self.fuelLevel()
        if float(fuel) < 500:
            res = await self.refuel()

            if res != "true":
                await self.gotTo(0, 0, 1, "backward")
                await self.grabFuel()
                await self.refuel()

                # Return to work
                await self.gotTo(self.lastX, self.lastY, self.lastZ, self.lastDirection)

    # Checks if the inventory is too full and empties
    async def checkInventoryFull(self):
        filled = await self.fullSpaces()
        
        if float(filled) > 14:
            await self.gotTo(0, 0, 0, "backward")
            await self.emptyAll()

            # Return to work
            await self.gotTo(self.lastX, self.lastY, self.lastZ, self.lastDirection)
            





