var id= 1;
for(var g=1; g<6;g++)
{
    var size = Math.floor(20*Math.random());
    var m =Math.floor(100*Math.random());
    for(var s=0; s<size;s++,id++)
    {
        db.agg.insertOne({
            _id:id,
            val : m*Math.random(),
            g:g
        })
    }

}