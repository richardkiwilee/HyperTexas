Score_Name_No_Pair = '高牌'
Score_Name_One_Pair = '对子'
Score_Name_Two_Pair = '两对'
Score_Name_Three = '三条'
Score_Name_Straight = '顺子'
Score_Name_Flush = '同花'
Score_Name_Full_House = '葫芦'
Score_Name_Four = '四条'
Score_Name_Straight_Flush = '同花顺'
Score_Name_Five = '五条'
Score_Name_House_Flush = '同花葫芦'
Score_Name_Five_Flush = '同花五条'


BASE_SCORE = {
    Score_Name_No_Pair: [5, 1],
    Score_Name_One_Pair: [10, 2],
    Score_Name_Two_Pair: [20, 2],
    Score_Name_Three: [30, 3],
    Score_Name_Straight: [30, 4],
    Score_Name_Flush: [35, 4],
    Score_Name_Full_House: [40, 4],
    Score_Name_Four: [60, 7],
    Score_Name_Straight_Flush: [100, 8],
    Score_Name_Five: [120, 12],
    Score_Name_House_Flush: [140, 14],
    Score_Name_Five_Flush: [160, 16],
}

LEVEL_BOUNS_SCORE = {
    Score_Name_No_Pair: [10, 1],
    Score_Name_One_Pair: [15, 1],
    Score_Name_Two_Pair: [20, 1],
    Score_Name_Three: [20, 2],
    Score_Name_Straight: [30, 2],
    Score_Name_Flush: [15, 2],
    Score_Name_Full_House: [25, 2],
    Score_Name_Four: [30, 3],
    Score_Name_Straight_Flush: [40, 3],
    Score_Name_Five: [35, 3],
    Score_Name_House_Flush: [40, 3] ,
    Score_Name_Five_Flush: [40, 3],
}
