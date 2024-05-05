sellprice = "350"

Player.HeadMessage(33, "Target an item inside the source container to show me the type")
item_example = Items.FindBySerial(Target.PromptTarget("Target an item",33))

source_container = Items.FindBySerial(item_example.Container)

Player.HeadMessage(33, "Target an item inside the container. I will place next to it")
start_item = Items.FindBySerial(Target.PromptTarget("Target an item inside the container. I will place next to it", 33))

dest_container = Items.FindBySerial(start_item.Container)

Items.UseItem(source_container)
Misc.Pause(500)
Items.UseItem(dest_container)
Misc.Pause(500)

#pouch
#x_start = 50 # pouch origin x
#y_start = 60 # pouch origin y

x_step = 10
y_step = 10
x_start = start_item.Position.X
y_start = start_item.Position.Y

x = x_start
y = y_start
for itm in source_container.Contains:
    if itm.ItemID == item_example.ItemID:
        x = x + x_step
        if x >= 150:
            x = x_start
            y = y + y_step
        
        Player.HeadMessage(33, f"{x} - {y}")
        Items.Move(itm.Serial, dest_container, 1, x, y)
        Misc.Pause(500)
        Misc.ResponsePrompt(sellprice)
        Misc.Pause(300)
        
            



#Items.Move(0x416AF554,0x40059839,1,10,10)
#Misc.Pause(500)
#Misc.ResponsePrompt("500")
