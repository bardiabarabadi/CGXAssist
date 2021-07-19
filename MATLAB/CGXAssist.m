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
    
    methods
        function obj = CGXAssist(targetName)
            %CGXASSIST Construct an instance of this class
            obj.targetName = targetName;
            obj.allRawDataCell = CStack();
            allRawDataArray = 0;
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
            disp("Got Value");
        end
        
        function obj = clearPackets(obj)
            obj.allRawDataArray = 0;
            obj.allRawDataCell = CStack();
        end
        
        
        function [batt] = getBattery(obj)
            
            while obj.allRawDataCell.isempty()
                disp("waiting for packets to calculate battery");
                obj.startStream();
                pause(1);
                obj.stopStream();
                obj.refresh();
            end
            
            lastSyncByteLocation = find(obj.allRawDataArray==255,1,'last');
            lastBattByteLocation = lastSyncByteLocation - 3;
            batt = 100*double(obj.allRawDataArray(lastBattByteLocation))...
                      /128.0;
        end
    end
end

