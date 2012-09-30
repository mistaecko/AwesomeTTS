'    Based on Peter Bennett's code
'
'    Code eddited by Arthur Helfstein Fragoso for the Plugin AwesomeTTS for Anki
'
'    GNU General Public License
'    <http://www.gnu.org/licenses/>.

doWaveFile = False
doMultWaveFiles = False
pFileName = Null            ' Name of output wav file
pUnicodeFileName = Null     ' name of input text file
rate=-999
volume=-999
samples=44100
channels=2
pVoice=Null
pEncoding = Null
needFileName = False
needRate = False
needVolume = False
needWord = False
needPron = False
needUnicodeFileName = False
needSamples = False
needChannels = False
needVoice = False
needEncoding = False
doInstruct = False
doLexiconAdd = False
doListVoices = False
isCscript = True        ' Identifies if we are running CScript
needDebugging = False

pVoice=Null
needVoice = False


dim tts
set tts = createobject("sapi.spvoice")


Dim argv
Set argv = WScript.Arguments




For Each arg in argv
    If needVoice Then
        pVoice=arg
	setVoice tts,pVoice
        needVoice = False
    ElseIf needFileName Then
        pFileName=arg
        needFileName = False
    ElseIf arg = "-voice" Then
        needVoice = True
    ElseIf arg = "-vl" Then
        doListVoices = True
    ElseIf arg = "-o" Then
        doWaveFile = True
        needFileName = True
    Else
        texttospeak = texttospeak  & " " & arg
    End If
Next


if doListVoices then
    Set voiceList = tts.getVoices
    list = "--Voice List--"
    For Each strVoice in voiceList
        list = list & vbLf
        list = list & strVoice.GetAttribute("Name")
    Next
    printOut(list)
    WScript.Quit (0)
End if

if Not IsNull(pFileName) Then
    If Len(pFileName) > 4 _
        And LCase(Mid(pFileName,Len(pFilename) -3)) = ".wav" Then
        pFileName = Mid(pFileName,1,Len(pFilename) -4)
    End If
    pFileName = pFileName & ".wav"

    Set outputFile = CreateObject("SAPI.SpFileStream")
    Set format = outputFile.format
    format.Type = getWaveType(samples,channels)
    Set outputFile.Format = format
    outputFile.Open pFileName, 3
    Set tts.AudioOutputStream = outputFile
End If


tts.speak texttospeak

Function getWaveType(samples, channels)
    getWaveType = 34
    If     samples =  8000 Then 
        getWaveType = 6
    ElseIf samples = 16000 Then 
        getWaveType = 18
    ElseIf samples = 22050 Then 
        getWaveType = 22
    ElseIf samples = 44100 Then 
        getWaveType = 34
    ElseIf samples = 48000 Then 
        getWaveType = 38
    Else
        printErr("Invalid samples "&samples)
    End If
    If channels = 1 Then
    ElseIf channels = 2 Then
        getWaveType = getWaveType + 1
    Else
        printErr("Invalid channel number "&channels)
    End If
End Function


Function setVoice(hSpeaker, voice)
    Set list = hSpeaker.GetVoices("Name="&voice)
    If list.Count <> 1 Then
        printOut("ERROR "&list.Count&" voices match "&voice)
        setVoice = False
        Exit Function
    End If
    Set hSpeaker.Voice = list.Item(0)
    setVoice = True
End Function


Sub printOut (text)
    if isCscript Then
	WScript.StdOut.Write text
    Else
        WScript.Echo text
    End If
End Sub
