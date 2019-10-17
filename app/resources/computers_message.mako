% for domain, computers in computers_group.items():
In domain ${ domain }:
    % for computer in computers:
${ computer.name } - [${ computer.username }]
    % endfor

% endfor
