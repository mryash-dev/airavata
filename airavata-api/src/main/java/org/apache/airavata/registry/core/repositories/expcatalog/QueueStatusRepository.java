/**
*
* Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements. See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership. The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License. You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied. See the License for the
* specific language governing permissions and limitations
* under the License.
*/
package org.apache.airavata.registry.core.repositories.expcatalog;

import com.github.dozermapper.core.Mapper;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.apache.airavata.model.status.QueueStatusModel;
import org.apache.airavata.registry.core.entities.expcatalog.QueueStatusEntity;
import org.apache.airavata.registry.core.utils.DBConstants;
import org.apache.airavata.registry.core.utils.ObjectMapperSingleton;
import org.apache.airavata.registry.core.utils.QueryConstants;
import org.apache.airavata.registry.cpi.RegistryException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class QueueStatusRepository extends ExpCatAbstractRepository<QueueStatusModel, QueueStatusEntity, String> {
    private static final Logger logger = LoggerFactory.getLogger(QueueStatusRepository.class);

    public QueueStatusRepository() {
        super(QueueStatusModel.class, QueueStatusEntity.class);
    }

    public boolean createQueueStatuses(List<QueueStatusModel> queueStatusModels) throws RegistryException {

        for (QueueStatusModel queueStatusModel : queueStatusModels) {
            Mapper mapper = ObjectMapperSingleton.getInstance();
            QueueStatusEntity queueStatusEntity = mapper.map(queueStatusModel, QueueStatusEntity.class);
            execute(entityManager -> entityManager.merge(queueStatusEntity));
        }

        return true;
    }

    public List<QueueStatusModel> getLatestQueueStatuses() throws RegistryException {
        List<QueueStatusModel> queueStatusModelList = select(QueryConstants.GET_ALL_QUEUE_STATUS_MODELS, 0);
        return queueStatusModelList;
    }

    public Optional<QueueStatusModel> getQueueStatus(String hostName, String queueName) throws RegistryException {
        Map<String, Object> queryParameters = new HashMap<>();
        queryParameters.put(DBConstants.QueueStatus.HOST_NAME, hostName);
        queryParameters.put(DBConstants.QueueStatus.QUEUE_NAME, queueName);
        List<QueueStatusModel> queueStatusModels = select(QueryConstants.FIND_QUEUE_STATUS, 1, 0, queryParameters);
        if (queueStatusModels != null && !queueStatusModels.isEmpty()) {
            return Optional.of(queueStatusModels.get(0));
        }
        return Optional.empty();
    }
}
