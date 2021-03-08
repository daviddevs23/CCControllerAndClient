host = "ws://localhost:8888"

ws, err = http.websocket(host)

--print("Where the bot is currently placed is the bottom, right")
--print("Please Enter a width")
--width = read()
--ws.send(width)
--
--print("Please Enter a depth")
--depth = read()
--ws.send(depth)
--
--print("Please Enter a height")
--height = read()
--ws.send(height)

run = true

while run do
    command = ws.receive()

    if command == "stop" then
        run = false
        ws.close()

    elseif command == "forward" then
        if turtle.forward() then
            ws.send("true")
        else
            ws.send("false")
        end

    elseif command == "back" then
        if turtle.back() then
            ws.send("true")
        else
            ws.send("false")
        end

    elseif command == "up" then
        if turtle.up() then
            ws.send("true")
        else
            ws.send("false")
        end

    elseif command == "down" then
        if turtle.down() then
            ws.send("true")
        else
            ws.send("false")
        end

    elseif command == "fuelLevel" then
        ws.send(turtle.getFuelLevel())

    elseif command == "refuel" then
        currentSlot = turtle.getSelectedSlot()
        turtle.select(16)
        result = turtle.refuel()
        turtle.select(currentSlot)
        ws.send(result)

    elseif command == "digUp" then
        ws.send(tostring(turtle.digUp()))

    elseif command == "digDown" then
        ws.send(tostring(turtle.digDown()))

    elseif command == "dig" then
        state = turtle.dig()

        while turtle.detect() do
            state = turtle.dig()
        end

        ws.send(tostring(state))

    elseif command == "right" then
        turtle.turnRight()
        ws.send("true")

    elseif command == "left" then
        turtle.turnLeft()
        ws.send("true")

    elseif command == "place" then
        ws.send(turtle.place())

    elseif command == "placeUp" then
        ws.send(turtle.placeUp())

    elseif command == "placeDown" then
        ws.send(turtle.placeDown())

    -- Returns the number of slots that are full
    elseif command == "fullSpaces" then
        count = 0
        for i=1,16,1 do
            if turtle.getItemCount(i) > 0 then
                count = count + 1
            end
        end

        ws.send(tostring(count))

    -- Get a string of the inventory
    elseif command == "getInventory" then
        inventory = ""

        for i=1,16,1 do
            item = turtle.getItemDetail(i)

            if item == nil then
                inventory = inventory .. "d;d"

            else 
                inventory = inventory .. tostring(item.name) .. ";" .. tostring(item.count)

            end

            inventory = inventory .. " "
        end

        ws.send(inventory)

    elseif command == "currentSlot" then
        ws.send(tostring(turtle.getSelectedSlot()))


    elseif command == "pickSlot" then
        ws.send("ready")

        slot = ws.receive()

        slot = tonumber(slot)
        ws.send(tostring(turtle.select(slot)))

    -- Empties all items except the last fuel slot into a chest
    elseif command == "emptyAll" then
        for i=1,15,1 do
            turtle.select(i) 
            turtle.drop()
        end

        ws.send("true")

    -- Grabs a whole stack of fuel and puts it in the last slot
    -- Last slot must be empty
    elseif command == "grabFuel" then
        currentSlot = turtle.getSelectedSlot()
        turtle.select(16)
        res = turtle.suck()
        turtle.select(currentSlot)
        ws.send(res)

    end
end
