import React, {useState} from 'react';
import './App.css';
import {Stack, Typography, TextField, Button} from "@mui/material";
import axios from "axios";

interface LogMetadata {
  parentResourceId: string
}

interface Log {
  level: string
  message: string
  resourceId: string
  timestamp: string
  traceId: string
  spanId: string
  commit: string
  metadata: LogMetadata
}

function TextBox(props: {label: string, value: string, setValue: React.Dispatch<React.SetStateAction<string>>}) {
  return <TextField
    type={'text'}
    style={{background: 'white', flex: 1}}
    value={props.value}
    label={props.label}
    onChange={e => props.setValue(e.target.value)}
  />
}

function App() {
  const [search, setSearch] = useState("")

  const [level, setLevel] = useState("")
  const [resourceId, setResourceId] = useState("")
  const [traceId, setTraceId] = useState("")
  const [spanId, setSpanId] = useState("")
  const [commit, setCommit] = useState("")
  const [metadataParentResourceId, setMetadataParentResourceId] = useState("")

  const [startTime, setStartTime] = useState("")
  const [endTime, setEndTime] = useState("")

  const [logs, setLogs] = useState<Log[]>([])



  const getLogs = () => {
    axios.post(
      "http://localhost:3000/query",
      {
        search: search === "" ? null : search,
        level: level === ""? null : level,
        resourceId: resourceId === ""? null : resourceId,
        timestamp_start: startTime === ""? null : startTime,
        timestamp_end: endTime === ""? null : endTime,
        traceId: traceId === ""? null : traceId,
        spanId: spanId === ""? null : spanId,
        commit: commit === ""? null : commit,
        metadata_parentResourceId: metadataParentResourceId === ""? null : metadataParentResourceId
      }).then(response => {
        if (response.status === 200)
          setLogs(response.data)
    })
  }

  return (
    <Stack>
      <Stack p={4} spacing={2} bgcolor={'rgba(0,0,255,0.1)'}>
        <TextBox value={search} label={'Search'} setValue={setSearch} />
        <Stack direction={'row'} spacing={2}>
          <TextBox value={level} label={'Level'} setValue={setLevel} />
          <TextBox value={resourceId} label={'Resource ID'} setValue={setResourceId} />
          <TextBox value={traceId} label={'Trace ID'} setValue={setTraceId} />
          <TextBox value={spanId} label={'Span ID'} setValue={setSpanId} />
          <TextBox value={commit} label={'Commit'} setValue={setCommit} />
          <TextBox value={metadataParentResourceId} label={'Parent Resource ID'} setValue={setMetadataParentResourceId} />
        </Stack>
        <Stack direction={'row'} spacing={2}>
          <TextBox value={startTime} label={'Start Time'} setValue={setStartTime} />
          <TextBox value={endTime} label={'End Time'} setValue={setEndTime} />
          <Button variant={'contained'} onClick={getLogs}>Apply</Button>
        </Stack>
      </Stack>
      <Stack p={4} spacing={2}>
        {logs.map(log => {
          return(
            <Stack p={2} bgcolor={'rgba(0,0,0,0.05)'}>
              <Stack direction={'row'} justifyContent={'space-between'} pb={1}>
                <Typography><b>[{log.level.toUpperCase()}]</b> {log.message}</Typography>
                <Typography>{log.timestamp}</Typography>
              </Stack>
              <Stack direction={'row'} justifyContent={'space-between'}>
                <Typography variant={'subtitle2'}>Resource ID: <b>{log.resourceId}</b></Typography>
                <Typography variant={'subtitle2'}>Parent Resource ID: <b>{log.metadata.parentResourceId}</b></Typography>
              </Stack>
              <Stack direction={'row'} justifyContent={'space-between'}>
                <Typography variant={'subtitle2'}>Trace ID: <b>{log.traceId}</b></Typography>
                <Typography variant={'subtitle2'}>Span ID: <b>{log.spanId}</b></Typography>
                <Typography variant={'subtitle2'}>Commit: <b>{log.commit}</b></Typography>
              </Stack>
            </Stack>
          )
        })}
      </Stack>
    </Stack>
  );
}

export default App;
