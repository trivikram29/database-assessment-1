SELECT id,
       HOST,
       db,
       command,
       TIME,
       state
                                , concat(char(39), @DMASOURCEID, char(39)) as DMA_SOURCE_ID, concat(char(39), @DMAMANUALID, char(39)) as DMA_MANUAL_ID
FROM information_schema.processlist
;
