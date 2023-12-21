db.aggtwo.aggregate([{ $group: { _id: { g1: "$g1", g2: "$g2" },avg: { $val: "$val" } }  }])


db.groups.aggregate([
    {
        $lookup: {
            from: 'agg', 
            localField: '_id', 
            foreignField: 'g', 
            as: 't'
        }, 
    }, {
           $set: {
              red: {
                $reduce: {
                    input: "$t",
                    initialValue: 0,
                    in: { $sum: [ "$$value", "$$this.val" ] }
                }
              }  
            }
        }
    ]
);



db.groups.aggregate([
    {
        $lookup: {
            from: 'agg', 
            localField: '_id', 
            foreignField: 'g', 
            as: 't'
        }, 
    }, {
           $set: {
              tn: {
                $map: {
                    input: "$t",
                    as: "v",
                    initialValue: 0,
                    in: { $sum: [ "$$value", "$$this.val" ] }
                }
              }  
            }
        }
    ]
);


