-- name: collection-postgres-bg-writer-stats
with src as (
    select w.checkpoints_timed,
        w.checkpoints_req as checkpoints_requested,
        w.checkpoint_write_time,
        w.checkpoint_sync_time,
        w.buffers_checkpoint,
        w.buffers_clean,
        w.maxwritten_clean as max_written_clean,
        w.buffers_backend,
        w.buffers_backend_fsync,
        w.buffers_alloc as buffers_allocated,
        w.stats_reset
    from pg_stat_bgwriter w
)
select :PKEY as pkey,
    :DMA_SOURCE_ID as dma_source_id,
    :DMA_MANUAL_ID as dma_manual_id,
    src.checkpoints_timed,
    src.checkpoints_requested,
    src.checkpoint_write_time,
    src.checkpoint_sync_time,
    src.buffers_checkpoint,
    src.buffers_clean,
    src.max_written_clean,
    src.buffers_backend,
    src.buffers_backend_fsync,
    src.buffers_allocated,
    src.stats_reset
from src;
