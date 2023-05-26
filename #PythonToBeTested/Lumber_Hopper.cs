//C#
using System;
using System.IO;
using System.Collections.Generic;
//using System.Windows.Forms;
//using System.Drawing;
 
namespace RazorEnhanced
{
    public class Lumberjacking
    {
        private static void Log(object messageString)
        {
            Misc.SendMessage(messageString, 201);
        }
 
        public static long UnixTimeStamp()
        {
            return (long)(DateTime.UtcNow - new DateTime(1970, 1, 1)).TotalMilliseconds;
        }
 
        public enum MapType
        {
            Felucca,
            Trammel,
            Ilshenar,
            Malas,
            Tokuno,
            TerMur
        }
 
        public enum NotorietyType
        {
            Black,
            Blue,
            Green,
            Greyish,
            Grey,
            Orange,
            Red,
            Yellow
        }
 
        public enum FlagType
        {
            None,
            Translucent,
            Wall,
            Damaging,
            Impassable,
            Surface,
            Bridge,
            Window,
            NoShoot,
            Foliage,
            HoverOver,
            Roof,
            Door,
            Wet
        }
 
        public enum ItemLayerType
        {
            RightHand,
            LeftHand,
            Shoes,
            Pants,
            Shirt,
            Head,
            Gloves,
            Ring,
            Neck,
            Waist,
            InnerTorso,
            Bracelet,
            MiddleTorso,
            Earrings,
            Arms,
            Cloak,
            OuterTorso,
            OuterLegs,
            InnerLegs,
            Talisman
        }
 
        public int DistanceToTile(int tilePosX, int tilePosY)
        {
            double powX = Math.Pow(Player.Position.X - tilePosX, 2);
            double powY = Math.Pow(Player.Position.Y - tilePosY, 2);
            int result = (int)Math.Round(Math.Pow(powX + powY, 0.5f));
 
            return result;
        }
 
        public struct TreeData
        {
            public int tree;
            public int X;
            public int Y;
            public int Z;
        }
 
 
        private Mobile mobilePlayer = Mobiles.FindBySerial(Player.Serial);
 
        
 
        private int itemID_hatchet = 0x0F43;
 
        public void Run()
        {
            Log("Script Started.....");
            
            Journal.Clear();
 
            List<TreeData> treePositionList = GenerateTreeLinePositionData();
            Log("treePositionList count: " + treePositionList.Count);
 
            for (int i = 0; i < treePositionList.Count; i++)
            {
                if (Player.Weight > Player.MaxWeight - 15)
                {
                    Log("Max weight reached...");
                    break;
                }
 
                Item hatchet = Player.GetItemOnLayer(ItemLayerType.LeftHand.ToString());
                if (hatchet == null)
                {
                    Log("No hatchet in hand");
                    break;
                }
 
                MoveToDestination(treePositionList[i]);
 
                HarvestWood(treePositionList[i]);
            }
 
            Log("Script Ended.....");
        }
 
        private List<TreeData> GenerateTreeLinePositionData()
        {
            List<TreeData> treeLinePositionData = new List<TreeData>();
 
            int pPosX = Player.Position.X;
            int pPosY = Player.Position.Y;
 
            for (int y = 0; y < 100; y++)
            {
                bool hasFoundTree = false;
 
                int landId = Statics.GetLandID(pPosX, pPosY - y, (int)MapType.Felucca);
                List<Statics.TileInfo> staticsTileInfoList = Statics.GetStaticsTileInfo(pPosX, pPosY - y, (int)MapType.Felucca);
 
                if (staticsTileInfoList.Count == 2)
                {
 
                    int treeStatic = 0;
                    int staticID_1 = staticsTileInfoList[0].StaticID;
                    int staticID_2 = staticsTileInfoList[1].StaticID;
 
                    if (staticID_2 == staticID_1 + 1)
                    {
                        treeStatic = staticID_1;
                        hasFoundTree = true;
                    }
                    else if (staticID_1 == staticID_2 + 1)
                    {
                        treeStatic = staticID_2;
                        hasFoundTree = true;
                    }
 
                    if (hasFoundTree == true)
                    {
                        TreeData positionDataObject = new TreeData();
                        positionDataObject.tree = treeStatic;
                        positionDataObject.X = pPosX;
                        positionDataObject.Y = pPosY - y;
                        positionDataObject.Z = Statics.GetLandZ(pPosX, pPosY - y, (int)MapType.Felucca);
 
                        treeLinePositionData.Add(positionDataObject);
                    }
                }
            }
 
            return treeLinePositionData;
        }
 
        private void MoveToDestination(TreeData positionData)
        {
            List<Tile> tileList = PathFinding.GetPath(positionData.X-1, positionData.Y, false);
            if (tileList == null)
            { return; }
 
            while (true)
            {
                if (tileList.Count == 0)
                { break; }
 
                bool isHouseTile = Statics.CheckDeedHouse(tileList[0].X, tileList[0].Y);
                if (isHouseTile == true)
                {
                    tileList.RemoveAt(0);
                    continue;
                }
 
                int targetPositionZ = Statics.GetLandZ(tileList[0].X, tileList[0].Y, (int)MapType.Felucca);
                Player.PathFindTo(tileList[0].X, tileList[0].Y, targetPositionZ);
 
                while (true)
                {
                    Misc.Pause(50);
                    int distance = DistanceToTile(tileList[0].X, tileList[0].Y);
                    if (distance <= 1)
                    {
                        tileList.RemoveAt(0);
                        break;
                    }
                }
            }
        }
 
        private void HarvestWood(TreeData treeData)
        {
            while(true)
            {
                if(Player.Weight > Player.MaxWeight-15)
                {
                    Log("Max weight reached...");
                    break;
                }
 
                Item hatchet = Player.GetItemOnLayer(ItemLayerType.LeftHand.ToString());
                if (hatchet == null)
                {
                    Log("No hatchet in hand");
                    break;
                }
 
                Player.HeadMessage(201, "CHOP");
                Items.UseItem(hatchet.Serial);
                Misc.Pause(250);
                Target.TargetExecute(treeData.X, treeData.Y, treeData.Z, treeData.tree);
                Misc.Pause(1500);
 
                string stringJournal = "There's not enough wood here to harvest.";
                if (Journal.Search(stringJournal) == true)
                {
                    Log(stringJournal);
                    Journal.Clear();
                    break;
                }
            }
        }
    }
}
 
 
 
 
//positionDataList.Clear();
 
 
//int startPosX = Player.Position.X - 3;
//int startPosY = Player.Position.Y + 3;
 
//int range = 7;
//for (int x = 0; x < range; x++)
//{
//    for (int y = 0; y < range; y++)
//    {
//        int tilePosX = startPosX + x;
//        int tilePosY = startPosY - y;
 
//        bool isHouseTile = Statics.CheckDeedHouse(tilePosX, tilePosY);
//        if (isHouseTile == true)
//        { continue; }
 
//        int landId = Statics.GetLandID(tilePosX, tilePosY, (int)MapType.Felucca);
//        bool isTileFlag_Impassable = Statics.GetTileFlag(landId, FlagType.Impassable.ToString());
 
//        List<Statics.TileInfo> staticsTileInfoList = Statics.GetStaticsTileInfo(tilePosX, tilePosY, (int)MapType.Felucca);
 
//        if (staticsTileInfoList.Count == 2)
//        {
//            bool isTree = false;
 
//            int staticID_1 = staticsTileInfoList[0].StaticID;
//            int staticID_2 = staticsTileInfoList[1].StaticID;
 
//            if (staticID_2 == staticID_1 + 1)
//            {
//                isTree = true;
//            }
//            else if (staticID_1 == staticID_2 + 1)
//            {
//                isTree = true;
//            }
 
//            if (isTree == true)
//            {
//                PositionData positionDataObject = new PositionData();
//                positionDataObject.X = tilePosX;
//                positionDataObject.Y = tilePosY;
//                int tilePosZ = Statics.GetLandZ(tilePosX, tilePosY, (int)MapType.Felucca);
//                positionDataObject.Z = tilePosX;
 
//                positionDataList.Add(positionDataObject);
//            }
//        }
//    }
//}