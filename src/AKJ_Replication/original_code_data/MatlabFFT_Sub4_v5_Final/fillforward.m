function fy=fillforward(y)
fy=y;
for j=1:size(y,2);
    nanind=find(isnan(y(:,j)));
    if ~isempty(nanind)
        for i=1:size(nanind,1)
            fy(nanind(i),j)=fy(nanind(i)-1,j);
        end
    end
end
return