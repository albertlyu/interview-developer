WITH player_woba AS (
    SELECT "Player" AS player
      , "Team" AS team
      , "PlayerId" AS player_id
      , "Pos" AS pos
      , (woba.wbb*("BB"-"IBB") + woba.whbp*"HBP" + woba.w1b*("H"-"2B"-"3B"-"HR") + woba.w2b*"2B" + woba.w3b*"3B" + woba.whr*"HR") AS woba_numerator
      , ("AB" + "BB" - "IBB" + "SF" + "HBP") AS woba_denominator
    FROM public.battingleaders batting
    JOIN public.woba_constants woba ON woba.season=2014 --join on woba_constants table only for 2014 season
  )
SELECT player
  , team
  , pos
  , woba_numerator / woba_denominator AS woba
FROM player_woba
ORDER BY woba_numerator / woba_denominator DESC;