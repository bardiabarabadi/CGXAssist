classdef CGXAssist
    %CGXASSIST Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        targetName
        deviceBleObj
        deviceBleChar
        allRawDataCell
        allRawDataArray
    end
    
    methods(Static)
        function [batt] = getBattery(dev)
            
            while dev.allRawDataCell.isempty()
                disp("waiting for packets to calculate battery");
                dev.startStream();
                pause(1);
                dev.stopStream();
                whos
                dev=dev.refresh();
                whos
            end
            
            lastSyncByteLocation = find(dev.allRawDataArray==255,1,'last');
            lastBattByteLocation = lastSyncByteLocation - 3;
            batt = 100*double(dev.allRawDataArray(lastBattByteLocation))...
                      /128.0;
        end
    end
    
    methods
        function obj = CGXAssist(targetName)
            %CGXASSIST Construct an instance of this class
            obj.targetName = targetName;
            obj.allRawDataCell = CStack();
        end
        
        function obj = findAndConnect(obj)
            blelist
            obj.deviceBleObj=ble(obj.targetName);
            obj.deviceBleChar=characteristic(obj.deviceBleObj, ...
                       "2456E1B9-26E2-8F83-E744-F34F01E9D701", ...
                       "2456E1B9-26E2-8F83-E744-F34F01E9D703");
            %c.Attributes
            handler=@(src,evt) obj.gotData(src,evt);
            obj.deviceBleChar.DataAvailableFcn = handler;
            
        end
        
        function startStream(obj)
            subscribe(obj.deviceBleChar);
        end
        function stopStream(obj)
            unsubscribe(obj.deviceBleChar);
            disp("Should be unsubscribed here");
        end
        
        function obj = refresh (obj)
            obj.allRawDataArray = cell2mat(obj.allRawDataCell.content());
        end
        
        
        function obj = gotData(obj, src, evt)
            [data, ts] = read(src, 'oldest');
            for i=1:size(data,2)
                obj.allRawDataCell.push(uint8(data(i)));
            end
        end
        
        function obj = clearPackets(obj)
            obj.allRawDataCell = CStack();
        end
        
        
        
    end
end

