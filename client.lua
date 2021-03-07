host = "ws://localhost:8888"

ws, err = http.websocket(host)

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

    end
end
