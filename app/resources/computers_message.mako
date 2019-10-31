% for domain, computers in computers_group.items():
В домене ${ domain }:
    % for computer in computers:
${ computer.name } - [${ computer.username }] (id = ${computer.mac_address})
    % endfor
% endfor
